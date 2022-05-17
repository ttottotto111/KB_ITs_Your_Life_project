from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post,Category,Tag,Comment
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django import forms

class PostList(ListView):
    model=Post
    paginate_by=10
    #template_name = 'blog/index.html'
class PostDetail(DetailView):
    model=Post

    def index(request):
        posts=Post.objects.all()
        return render(
            request,
             'blog/index.html',
         {
               'posts': posts,
        }
   )

    def get_context_data(self,**kwargs):
        context=super(PostDetail,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count()
        context['comment_form']=CommentForm
        return context

def single_post_page(request,pk):
    post=Post.objects.get(pk=pk)
    
    return render(request,
                  'blog/single_post_page.html',
                  {
                      'post': post,
                  })
def category_page(request,slug):
    if slug == 'no_category':
        category='미분류'
        post_list=Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            
        }
    )

    
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView,forms.ModelForm):
    model=Post
    fields=['생산지','브랜드','차종','category','차사진','가격','연식','주행거리','연료','구동방식','연비','배기량','색상','압류및저당','사고유무','전속이력','내용']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def get_form(self, form_class=None):
        form = super(PostCreate, self).get_form(form_class)
        form.fields['차종'].widget = forms.TextInput(attrs={'placeholder': 'ex)더뉴K7 더뉴모닝'})
        form.fields['가격'].widget = forms.TextInput(attrs={'placeholder': 'ex)1470만원'})
        form.fields['연식'].widget = forms.TextInput(attrs={'placeholder': 'ex)20년03월'})
        form.fields['주행거리'].widget = forms.TextInput(attrs={'placeholder': 'ex) 1,346km'})
        form.fields['연비'].widget = forms.TextInput(attrs={'placeholder': 'ex) 14.3km'})
        form.fields['배기량'].widget = forms.TextInput(attrs={'placeholder': 'ex) 346cc'})
        form.fields['색상'].widget = forms.TextInput(attrs={'placeholder': 'ex) 흰색'})
        form.fields['내용'].widget = forms.TextInput(attrs={'placeholder': 'ex) *인사말안녕하세요, 반갑습니다.많은 분들이 싸고 좋은 중고차만을 찾으십니다.그렇지만 무조건 싸고 좋은차는 없습니다.'})  
        return form
        
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser):
            form.instance.author=current_user
            response = super(PostCreate, self).form_valid(form) 
            
            return response
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields=['생산지','브랜드','차종','category','차사진','가격','연식','주행거리','연료','구동방식','연비','배기량','색상','압류및저당','사고유무','전속이력','내용']
    
    template_name='blog/post_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()


        return context
    
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        return response

    
def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)
    else:
        raise PermissionDenied
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST) 
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(차종__contains=q)  )
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']

        return context
    

# Create your views here.
