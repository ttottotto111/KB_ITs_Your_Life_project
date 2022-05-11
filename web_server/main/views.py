import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from blog.models import Post
from .models import *

# Create your views here.
def main(request):
    posts = Post.objects.all().order_by('-pk')
    maker = ['현대', '기아']
    h = ['그랜저', '소나타', '투싼']
    g = ['k5', 'k7', 'ev6']
    
    return render(request,"main/main.html",
                  {
                      'posts':posts,
                      'maker':maker,
                      'h': h,
                      'g':g
                  })

def car_maker(request, maker):
    if(maker == "hyundae"):
        data = {
            '차종': ['그랜저', '소나타', '투싼']
        }
        return JsonResponse(data)