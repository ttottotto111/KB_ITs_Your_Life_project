from django.shortcuts import render
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.core.paginator import Paginator  

def mypage(request, pk):
    user_name = User.objects.get(pk = pk)
    page = request.GET.get('page', '1')
        
    #게시글이 있는경우
    posts = Post.objects.filter(author_id = pk).order_by('-pk')
    comment = Comment.objects.filter(author_id = pk).order_by('-pk')
    
    post_page = Paginator(posts, 5)
    comment_page = Paginator(comment,3)
    
    post_obj = post_page.get_page(page)
    comment_obj = comment_page.get_page(page)
    context = {
        'name' :user_name,
        'posts': post_obj,
        'comment':comment_obj
        }
    return render(request,"mypage/mypage.html",context
                # {
                #     'name' :user_name,
                #     'posts':posts,
                #     'comment':comment
                # }
                )