from django.shortcuts import render, redirect
from blog.models import Post

# Create your views here.
def main(request):
    posts = Post.objects.all().order_by('-pk')
    
    return render(request,"main/main.html",
                  {
                      'posts':posts
                  })