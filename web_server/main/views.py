import enum
from turtle import down
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
    company = car_list.objects.values('company').distinct().order_by('company')
    
    return render(request,"main/main.html",
                  {
                      'posts':posts,
                      'maker':company,
                  })

def car_maker(request, pk):
    # 회사명으로 검색
    make = car_list.objects.filter(company=pk)
    name = make.values('name').distinct().order_by('name')
        
    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['name']

    # json형식으로 전송
    return JsonResponse(dict_m)

def car_detail(request, car_name):
    # 차종으로 검색
    make = car_list.objects.filter(name=car_name)
    name = make.values('name_detail').distinct().order_by('name_detail')

    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['name_detail']

    # json형식으로 전송
    return JsonResponse(dict_m)

# 감가 그래프 정보 전송
def car_chart(request, car_name, detail_no):
    # 차종, 감가율, 매년가격, 년도
    # 차종으로 검색
    car = car_list.objects.filter(name=car_name)
    car_info = car.values('name_detail', 'down_rate', 'rate_2023', 'rate_2024', 'rate_2025', 'rate_2026', 'rate_2027').distinct().order_by('name_detail')[detail_no]

    print("car info : ", car_info)
    
    #차종
    name = car_info['name_detail']
    #감가율
    down_rate = car_info['down_rate']
    #매년 가격
    price = []
    for i in range(3, 8):
        price.append(car_info['rate_202'+str(i)])
        
    # 딕셔너리에서 차종만 추출
    chart = {
        'name': name,
        'down_rate': down_rate,
        'price':price
    }

    # json형식으로 전송
    return JsonResponse(chart)