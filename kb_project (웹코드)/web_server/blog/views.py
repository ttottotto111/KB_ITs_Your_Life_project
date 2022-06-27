from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post,Category,Tag,Comment, car
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django import forms
from django.http import JsonResponse
from main.models import car_list
import xgboost as xgb
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
import cv2
from django.core.files.storage import default_storage

class PostList(ListView):
    model=Post
    ordering = '-pk'
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

def remove_post(request, pk):
    posts = Post.objects.get(pk=pk)
    if request.method == 'POST':
        posts.delete()
        return redirect('/blog/')
    return render(request, 'blog/delete.html', {'posts': posts})
    
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

class PostCreate( CreateView,forms.ModelForm):
    model=Post
    fields=['차사진','생산지','브랜드','차종','세부차종','category','연식','주행거리','연료','구동방식','배기량','색상','압류및저당','사고유무','전속이력','내용','가격']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def get_form(self, form_class=None):
        form = super(PostCreate, self).get_form(form_class)
        form.fields['가격'].widget = forms.TextInput(attrs={'placeholder': 'ex) 가격 알아보기를 클릭 후 적정가격을 알아본 후 입력해 주세요 만원을 제외하고 입력하여 주세요 '})
        form.fields['연식'].widget = forms.TextInput(attrs={'placeholder': 'ex)2017 년도만 입력하여 주세요'})
        form.fields['주행거리'].widget = forms.TextInput(attrs={'placeholder': 'ex) 1346 km를 제외하고 입력하여 주세요'})
        form.fields['배기량'].widget = forms.TextInput(attrs={'placeholder': 'ex) 346 cc를 제외하고 입력하여 주세요'})
        form.fields['색상'].widget = forms.TextInput(attrs={'placeholder': 'ex) 흰색'})
        form.fields['내용'].widget = forms.TextInput(attrs={'placeholder': 'ex) *인사말 안녕하세요, 반갑습니다.많은 분들이 싸고 좋은 중고차만을 찾으십니다.그렇지만 무조건 싸고 좋은차는 없습니다.'})  
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
    fields=['차사진','생산지','브랜드','차종','세부차종','category','연식','주행거리','연료','구동방식','배기량','색상','압류및저당','사고유무','전속이력','내용','가격']
    
    template_name='blog/post_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()


        return context
    
    def get_form(self, form_class=None):
        form = super(PostUpdate, self).get_form(form_class)
        form.fields['가격'].widget = forms.TextInput(attrs={'placeholder': 'ex) 가격 알아보기를 클릭 후 적정가격을 알아본 후 입력해 주세요 만원을 제외하고 입력하여 주세요'})
        form.fields['연식'].widget = forms.TextInput(attrs={'placeholder': 'ex) 2017 년도만 입력하여 주세요'})
        form.fields['주행거리'].widget = forms.TextInput(attrs={'placeholder': 'ex) 1346 km를 제외하고 입력하여 주세요'})
        form.fields['배기량'].widget = forms.TextInput(attrs={'placeholder': 'ex) 346 cc를 제외하고 입력하여 주세요'})
        form.fields['색상'].widget = forms.TextInput(attrs={'placeholder': 'ex) 흰색'})
        form.fields['내용'].widget = forms.TextInput(attrs={'placeholder': 'ex) *인사말 안녕하세요, 반갑습니다.많은 분들이 싸고 좋은 중고차만을 찾으십니다.그렇지만 무조건 싸고 좋은차는 없습니다.'})  
        return form
    
    
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
            Q(세부차종__contains=q) | Q(브랜드__contains=q))
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']

        return context
    

# Create your views here.
def car_maker(request, pk):
    # 회사명으로 검색
    print(pk)
    make = car_list.objects.filter(made=pk)
    name = make.values('company').distinct().order_by('company')
        
    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['company']

    # json형식으로 전송
    return JsonResponse(dict_m)


def car_brand(request, car_name):
    # 차종으로 검색
    print(car_name)
    make = car_list.objects.filter(company=car_name)
    name = make.values('name').distinct().order_by('name')

    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['name']

    # json형식으로 전송
    return JsonResponse(dict_m)

def car_detail(request, car_deta):
    # 차종으로 검색
    print(car_deta)
    make = car_list.objects.filter(name=car_deta)
    name = make.values('name_detail').distinct().order_by('name_detail')
    # 딕셔너리에서 차종만 추출
    dict_u = {}
    for i,mm in enumerate(name):
        dict_u[i]=mm['name_detail']

    # json형식으로 전송
    return JsonResponse(dict_u)


def car_lee(request, lee):
    # 차종으로 검색
    my_list = lee.split('_')
    print(my_list)
    df=pd.read_csv('blog/신차 가격표.csv')
    df2=pd.read_csv('blog/sebu_model2.csv')
    new_car_price=int(df[df['세부차종']==my_list[3]]['가격'])
    car_kind=str(df[df['세부차종']==my_list[3]]['차종'])
    
    if my_list[0]=='국산차':
        xgb_model=xgb.XGBRegressor()
        xgb_model=pickle.load(open('blog/x_model.model','rb'))
        xgb_korean_info=[0 for i in range(37)]
        xgb_korean_info[0]=int(my_list[8])
        xgb_korean_info[1]=int(my_list[4])
        xgb_korean_info[2]=int(my_list[5])
        if my_list[-3]=='있음':
            xgb_korean_info[3]=1
        if my_list[-2]=='있음':
            xgb_korean_info[4]=1
        if my_list[-1]=='있음':
            xgb_korean_info[5]=1
        
        car_color=my_list[-4]
        if car_color=='검정색':
            xgb_korean_info[6]=1
        elif car_color=='다크그레이색':
            xgb_korean_info[7]=1
        elif car_color=='은색':
            xgb_korean_info[8]=1
        elif car_color=='쥐색':
            xgb_korean_info[9]=1
        elif car_color=='진주색':
            xgb_korean_info[10]=1
        elif car_color=='청색':
            xgb_korean_info[11]=1
        elif car_color=='회색':
            xgb_korean_info[12]=1
        elif car_color=='흰색':
            xgb_korean_info[13]=1
            
        fuel_type=my_list[6]
        if fuel_type=='LPG':
            xgb_korean_info[14]=1
        elif fuel_type=='경유':
            xgb_korean_info[15]=1
        elif fuel_type=='경유+전기':
            xgb_korean_info[16]=1
        elif fuel_type=='수소전기':
            xgb_korean_info[17]=1
        elif fuel_type=='전기':
            xgb_korean_info[18]=1
        elif fuel_type=='하이브리드':
            xgb_korean_info[19]=1
        elif fuel_type=='휘발유':
            xgb_korean_info[20]=1
        elif fuel_type=='휘발유+LPG':
            xgb_korean_info[21]=1
        
        xgb_korean_info[23]=1
        wheel_type=my_list[-6]
        if wheel_type=='4륜':
            xgb_korean_info[24]=1
        elif wheel_type=='전륜':
            xgb_korean_info[25]=1
        elif wheel_type=='후륜':
            xgb_korean_info[26]=1
        
        if car_kind=='승용차':
            xgb_korean_info[27]=1
        elif car_kind=='승합차':
            xgb_korean_info[28]=1
        elif car_kind=='화물차':
            xgb_korean_info[29]=1
        
        car_brand=my_list[1]
        if car_brand=='기아':
            xgb_korean_info[30]=1
        elif car_brand=='대형트럭(2톤이상)':
            xgb_korean_info[31]=1
        elif car_brand=='르노삼성':
            xgb_korean_info[32]=1
        elif car_brand=='쉐보레':
            xgb_korean_info[33]=1
        elif car_brand=='쌍용':
            xgb_korean_info[34]=1
        elif car_brand=='제네시스':
            xgb_korean_info[35]=1
        elif car_brand=='현대':
            xgb_korean_info[36]=1
        
        xgb_korean_info=np.array([xgb_korean_info])
        res=xgb_model.predict(xgb_korean_info)
        res=list(res)[0]*new_car_price
        res=str(int(res))
        print(res)
    
    elif my_list[0]=='외제차':
        xgb_model=xgb.XGBRegressor()
        xgb_model=pickle.load(open('blog/x_modelf.model','rb'))
        xgb_korean_info=[0 for i in range(66)]
        xgb_korean_info[0]=int(my_list[8])
        xgb_korean_info[1]=int(my_list[4])
        xgb_korean_info[2]=int(my_list[5])
        if my_list[-3]=='있음':
            xgb_korean_info[3]=1
        if my_list[-2]=='있음':
            xgb_korean_info[4]=1
        if my_list[-1]=='있음':
            xgb_korean_info[5]=1
        
        car_color=my_list[-4]
        if car_color=='검정색':
            xgb_korean_info[6]=1
        elif car_color=='다크그레이색':
            xgb_korean_info[7]=1
        elif car_color=='은색':
            xgb_korean_info[8]=1
        elif car_color=='쥐색':
            xgb_korean_info[9]=1
        elif car_color=='진주색':
            xgb_korean_info[10]=1
        elif car_color=='청색':
            xgb_korean_info[11]=1
        elif car_color=='회색':
            xgb_korean_info[12]=1
        elif car_color=='흰색':
            xgb_korean_info[13]=1
            
        fuel_type=my_list[6]
        if fuel_type=='LPG':
            xgb_korean_info[14]=1
        elif fuel_type=='경유':
            xgb_korean_info[15]=1
        elif fuel_type=='경유+전기':
            xgb_korean_info[16]=1
        elif fuel_type=='수소전기':
            xgb_korean_info[17]=1
        elif fuel_type=='전기':
            xgb_korean_info[18]=1
        elif fuel_type=='하이브리드':
            xgb_korean_info[19]=1
        elif fuel_type=='휘발유':
            xgb_korean_info[20]=1
        elif fuel_type=='휘발유+LPG':
            xgb_korean_info[21]=1
        
        xgb_korean_info[23]=1 # 수동, 자동
        
        wheel_type=my_list[-6]
        if wheel_type=='4륜':
            xgb_korean_info[24]=1
        elif wheel_type=='전륜':
            xgb_korean_info[25]=1
        elif wheel_type=='후륜':
            xgb_korean_info[26]=1
        
        if car_kind=='승용차':
            xgb_korean_info[27]=1
        elif car_kind=='승합차':
            xgb_korean_info[28]=1
        elif car_kind=='화물차':
            xgb_korean_info[29]=1
        
        tmp_dic={'BMW':30,'닛산' : 31,'닷지':32,'대형버스(16인승)':33,'도요타':34,'람보르기니':35,'랜드로버':36,'렉서스':37,
                 '롤스로이스':38,'링컨':39,'마세라티':40,'미니':41,'미쯔비시':42,'벤츠':43,'벤틀리':44,'볼보':45,'북기은상':46,'선롱':47,
                 '스마트':48,'시트로엥':49,'아우디':50,'에스턴마틴':51,'인피니티':52,'재규어':53,'지프':54,'캐딜락':55,'크라이슬러':56,'테슬라':57,
                 '토요타':58,'포드':59,'포르쉐':60,'폭스바겐':61,'푸조':62,'피아트':63,'험머':64,'혼다':65}
        
        car_brand=my_list[1]
        xgb_korean_info[tmp_dic[car_brand]]=1
        
        
        xgb_korean_info=np.array([xgb_korean_info])
        res=xgb_model.predict(xgb_korean_info)
        res=list(res)[0]*new_car_price
        res=str(int(res))
        print(res)
                
    dict_lee = {'health': res}
  
    
    

    # json형식으로 전송
    return JsonResponse({'차 가격': res})


def car_tensor(request):
     if request.method == "POST":
        if request.FILES['uploadFile']:
            upload_image = request.FILES['uploadFile']
            default_storage.save("test" + '/' + upload_image.name, upload_image)
            
            new_model=tf.keras.models.load_model('blog\cnn.h5')
            tmp_images=cv2.imread(r'_media\test\{}'.format(upload_image.name),cv2.IMREAD_GRAYSCALE)
            img_input=tmp_images.copy()

            img=cv2.cvtColor(img_input,cv2.COLOR_GRAY2RGB)
            img_rgb=img.copy()
            img_rgb=(img_rgb/255.).astype(np.float32)
            img_lab=cv2.cvtColor(img_rgb,cv2.COLOR_RGB2Lab)

            img_1=img_lab[:,:,0]
            input_img=cv2.resize(img_1,(28,28))
            input_img-=50
            test=[]
            test.append(input_img)
            test=np.array(test)
            idx=np.argmax(new_model.predict(test)[0])
            car_dict={0:'K9',1:'카니발',2:'싼타페',3:'스포티지'}
            
            return_dict = {}
            return_dict['car'] = car_dict[idx]
            
            print(return_dict)
            return JsonResponse(return_dict)
        
        else:
            return JsonResponse({'car':'사진을 선택해 주세요.'})