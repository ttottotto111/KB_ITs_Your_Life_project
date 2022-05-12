import enum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from blog.models import Post
from .models import *

# Create your views here.
def main(request):
    # 게시판항목 최근 5개만 추출
    posts = Post.objects.all().order_by('-pk')[:3]
    
    # 차량검색의 회사명 추출 (중복항목 제거)
    maker = car_list_test.objects.values('maker').distinct().order_by('maker')
     
    
    return render(request,"main/main.html",
                  {
                      'posts':posts,
                      'maker':maker,
                  })

def car_maker(request, pk):
    print(pk)
    # 회사명으로 검색
    make = car_list_test.objects.filter(maker=pk)
    
    # 검색한 내용을 딕셔너리로 반환
    maker_dict =[]
    for m in make:
        maker_dict.append(model_to_dict(m))
    
    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(maker_dict):
        dict_m[i]=mm['car_list']
    
    # json형식으로 전송
    return JsonResponse(dict_m)