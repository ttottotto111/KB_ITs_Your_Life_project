import json
from django.shortcuts import render, redirect
from blog.models import Post

# Create your views here.
def main(request):
    posts = Post.objects.all().order_by('-pk')
    
    return render(request,"main/main.html",
                  {
                      'posts':posts
                  })

def car_maker(request):
    if request.method == 'POST':
        #테스트용 포스트파일
        posts = Post.objects.all().order_by('-pk')
        
        data = request.POST
        maker = data.get('maker')
        if(maker=="현대"):
            return render(request, "blog/post_list.html",
                        {
                            'maker':posts
                        })