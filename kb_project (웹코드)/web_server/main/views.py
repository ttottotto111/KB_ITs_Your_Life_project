import enum
from turtle import down
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from blog.models import Post
from .models import *
from django.contrib.auth.models import User
from mypage.models import Mypage
from django.db.models import Q

# Create your views here.
def main(request):
    # 게시판항목 최근 5개만 추출
    posts = Post.objects.all().order_by('-pk')
    posts = posts.exclude(category_id = 4)[:5]
    
    # 차량검색의 회사명 추출 (중복항목 제거)
    company = car_list.objects.values('company').distinct().order_by('company')
    
    return render(request,"main/main.html",
                  {
                      'posts':posts,
                      'maker':company,
                  })

#로그인했을시 게시물
def login_main(request, id):
    
    #유저 정보가 있을경우 (마이페이지 기준)
    if Mypage.objects.filter(author_id=id):
        user = Mypage.objects.filter(author_id=id)
        f_car = user.values('favorite_car')
        
        # 선호차량이 있을경우
        if f_car.values()[0]['favorite_car'] != None:
            
            #유사차량 검색
            c_name = car_name.objects.filter(model = f_car.values()[0]['favorite_car'])
            
            # 관심차량 및 1~5순위 추출
            favor = f_car.values()[0]['favorite_car']
            one = c_name.values()[0]['first']
            two = c_name.values()[0]['second']
            three = c_name.values()[0]['third']
            four = c_name.values()[0]['fourth']
            five = c_name.values()[0]['fiveth']
            
            #게시물 전체
            posts = Post.objects.all().order_by('-pk')
            posts = posts.exclude(category_id = 4)
            
            # 유사 차량 총 개수
            car_count = 0
            c_list = [favor, one, two, three, four, five]
            
            print(c_list)
            #유사차량이 있을경우
            if one != -1:
                #딕셔너리에 개수 추가
                for i in range(0,6):
                    car_count += posts.filter(세부차종 = c_list[i]).count()
                print(car_count)
                #세부차량 관련 게시글이 1개이상일 경우
                if car_count >0:
                    # 게시글이 5개 이상일 경우
                    if car_count >=5:
                        same_post = posts.filter(세부차종 = c_list[0]) | posts.filter(세부차종 = c_list[1]) |posts.filter(세부차종 = c_list[2]) | posts.filter(세부차종 = c_list[3]) | posts.filter(세부차종 = c_list[4])
                        same_post = same_post.order_by('-pk')[:5]
                        post_detail = same_post.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')
                        post_dic = {}
                        for i,p in enumerate(post_detail):
                            # 제목
                            title = p['브랜드']+ " " +p['세부차종']
                            
                            #유저이름
                            user_id = p['author_id']
                            user_name = User.objects.get(pk = user_id)
                            
                            # 포스트 번호
                            blog = p['id']
                            
                            post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                        return JsonResponse(post_dic)
                        
                    # 게시글이 5개보다 적을경우
                    else:
                        same_post = posts.filter(세부차종 = c_list[0]) | posts.filter(세부차종 = c_list[1]) |posts.filter(세부차종 = c_list[2]) | posts.filter(세부차종 = c_list[3]) | posts.filter(세부차종 = c_list[4])
                        same_post = same_post.order_by('-pk')
                        post_detail = same_post.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')

                        post_dic = {}
                        for i,p in enumerate(post_detail):
                            # 제목
                            title = p['브랜드']+ " " +p['세부차종']

                            #유저이름
                            user_id = p['author_id']
                            user_name = User.objects.get(pk = user_id)
                            
                            # 포스트 번호
                            blog = p['id']
                            
                            post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                        return JsonResponse(post_dic)
                              
                # 세부차량관련 게시글이 0개일경우        
                else:
                    post_detail = posts.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')[:5]

                    post_dic = {}
                    for i,p in enumerate(post_detail):
                        # 제목
                        title = p['브랜드']+ " " +p['세부차종']
                        
                        #유저이름
                        user_id = p['author_id']
                        user_name = User.objects.get(pk = user_id)
                        
                        # 포스트 번호
                        blog = p['id']
                        
                        post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                    return JsonResponse(post_dic)
                
            # 유사차량이 없을경우
            else:
                favor_car = posts.filter(세부차종=f_car.values()[0]['favorite_car'])
                
                #선호차량 게시물이 없을경우
                if favor_car.count() ==0:
                    post_detail = posts.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')[:5]
                    
                    post_dic = {}
                    for i,p in enumerate(post_detail):
                        # 제목
                        title = p['브랜드']+ " " +p['세부차종']
                        
                        #유저이름
                        user_id = p['author_id']
                        user_name = User.objects.get(pk = user_id)
                        
                        # 포스트 번호
                        blog = p['id']
                        
                        post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                    return JsonResponse(post_dic)
                
                #선호차량 게시물이 있을경우
                elif favor_car.count()>=5:
                    favor_post = posts.filter(세부차종 = favor_car)
                    favor_post = favor_post.order_by('-pk')[:5]
                    post_detail = favor_post.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')
                    
                    post_dic = {}
                    for i,p in enumerate(post_detail):
                        # 제목
                        title = p['브랜드']+ " " +p['세부차종']
                        
                        #유저이름
                        user_id = p['author_id']
                        user_name = User.objects.get(pk = user_id)
                        
                        # 포스트 번호
                        blog = p['id']
                        
                        post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                    return JsonResponse(post_dic)
                
                else:
                    favor_post = posts.filter(세부차종 = favor_car)
                    favor_post = favor_post.order_by('-pk')
                    post_detail = favor_post.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')
                    
                    post_dic = {}
                    for i,p in enumerate(post_detail):
                        # 제목
                        title = p['브랜드']+ " " +p['세부차종']
                        
                        #유저이름
                        user_id = p['author_id']
                        user_name = User.objects.get(pk = user_id)
                        
                        # 포스트 번호
                        blog = p['id']
                        
                        post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
                    return JsonResponse(post_dic)
        
        #선호차량이 없을경우
        else:
            posts = Post.objects.all().order_by('-pk')[:5]
            post_detail = posts.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')

            post_dic = {}
            for i,p in enumerate(post_detail):
                # 제목
                title = p['브랜드']+ " " +p['세부차종']
                
                #유저이름
                user_id = p['author_id']
                user_name = User.objects.get(pk = user_id)
                
                # 포스트 번호
                blog = p['id']
                
                post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
            return JsonResponse(post_dic)
    
    #유저정보가 없을경우
    else:
        posts = Post.objects.all().order_by('-pk')[:5]
        post_detail = posts.values('id', 'author_id','브랜드','차종','세부차종', 'created_at')
    
        post_dic = {}
        for i,p in enumerate(post_detail):
            # 제목
            title = p['브랜드']+ " " +p['세부차종']
                
            #유저이름
            user_id = p['author_id']
            user_name = User.objects.get(pk = user_id)
                
            # 포스트 번호
            blog = p['id']
                
            post_dic[i] = [title ,str(user_name) ,str(p['created_at'].date()), f"/blog/{blog}", f'/mypage/{user_id}']
        return JsonResponse(post_dic)

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
    car_info = car.values('name_detail', 'down_rate', 
                          'present_down','down1','down2','down3','down4','down5',
                          'present_value','value1','value2','value3','value4','value5',
                          'present_sub','sub1','sub2','sub3','sub4','sub5').distinct().order_by('name_detail')[detail_no]
    
    #차종
    name = car_info['name_detail']
    #감가율
    down_rate = car_info['down_rate']
    
    #매년 감가 가격
    down_price = []
    down_price.append(car_info['present_down'])
    for i in range(1, 6):
        down_price.append(car_info['down'+str(i)])
        
    #매년 잔존 가치율
    value_price = []
    value_price.append(car_info['present_value'])
    for i in range(1, 6):
        value_price.append(car_info['value'+str(i)])
        
    #감가가격과 잔존 가치율의 차이(판매 이득 가치)
    sub_price = []
    sub_price.append(car_info['present_sub'])
    for i in range(1, 6):
        sub_price.append(car_info['sub'+str(i)])
        
    # 딕셔너리에서 차종만 추출
    chart = {
        'name': name,
        'down_rate': down_rate,
        'price':down_price,
        'value': value_price,
        'sub': sub_price
    }

    # json형식으로 전송
    return JsonResponse(chart)