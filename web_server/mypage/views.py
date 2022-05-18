from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from main.models import car_list
from .models import Mypage

def mypage(request, pk):
    user_name = User.objects.get(pk = pk)
    company = car_list.objects.values('company').distinct().order_by('company')
    p_page = request.GET.get('p_page', '1')
    c_page = request.GET.get('c_page', '1')
        
    #게시글이 있는경우
    posts = Post.objects.filter(author_id = pk).order_by('-pk')
    comment = Comment.objects.filter(author_id = pk).order_by('-pk')
    
    post_page = Paginator(posts, 5)
    comment_page = Paginator(comment,3)
    
    post_obj = post_page.get_page(p_page)
    comment_obj = comment_page.get_page(c_page)
    
    #이미지 및 자기소개, 관심차량
    try:
        if Mypage.objects.get(author_id=pk):
            userinfo = Mypage.objects.get(author_id=pk)
        else:
            userinfo=None
    except:
        userinfo=None
        
    context = {
        'name' :user_name,
        'posts': post_obj,
        'comment':comment_obj,
        'userinfo': userinfo,
        'maker': company
        }
    return render(request,"mypage/mypage.html",context)

# 자기소개 변경
def user_content(request,pk):
    if request.method == "POST":
        # 사용자 데이터가 존재하는경우
        if Mypage.objects.filter(author_id = pk):
            usercontent = Mypage.objects.get(author_id=pk)
            # 자기소개가 있는경우
            if request.POST["user_content"]:
                usercontent.content = request.POST["user_content"]
                usercontent.save()
                return mypage(request, pk)
            
            # 자개소개가 없는경우
            else:
                return mypage(request, pk)
            
        # 사용자 데이터가 없는경우
        else:
            user_id = User.objects.get(pk=pk)
            usercontent = Mypage()
            # 자기소개가 있는경우
            if request.POST["user_content"]:
                Mypage.objects.create(author=user_id, content=request.POST["user_content"])
                return mypage(request, pk)
            
            # 자기소개가 없는경우 
            else:
                Mypage.objects.create(author=user_id, content=request.POST["user_content"])
                return mypage(request, pk)

# 이미지 변경
def user_img(request, pk):
    
    if request.method == "POST":
        # 사용자 데이터가 존재하는경우
        if Mypage.objects.filter(author_id = pk):
            userimg = Mypage.objects.get(author_id=pk)
            
            # 사진이 있는경우
            if request.FILES['user_img']:  
                userimg.profile_img = request.FILES['user_img']
                
                userimg.save()
                return mypage(request, pk)
            
            # 사진이 없는경우
            else:
                return mypage(request, pk)
            
        # 사용자 데이터가 없는경우
        else:
            user_id = User.objects.get(pk=pk)
            userimg = Mypage()
            # 사진이 있는경우
            if request.FILES['user_img']:  
                Mypage.objects.create(author=user_id, profile_img=request.FILES['user_img'])
                return mypage(request, pk)
            
            # 사진이 없는경우
            else:
                Mypage.objects.create(author=user_id, profile_img=request.FILES['user_img'])
                return mypage(request, pk)

            
#차종
def car_name(request, maker):
        # 차종으로 검색
    make = car_list.objects.filter(company=maker)
    name = make.values('name').distinct().order_by('name')

    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['name']

    # json형식으로 전송
    return JsonResponse(dict_m)

#세부차종
def car_detail(request, car):

    # 차종으로 검색
    make = car_list.objects.filter(name=car)
    name = make.values('name_detail').distinct().order_by('name_detail')

    # 딕셔너리에서 차종만 추출
    dict_m = {}
    for i,mm in enumerate(name):
        dict_m[i]=mm['name_detail']

    # json형식으로 전송
    return JsonResponse(dict_m)

#관심차종 등록
def favorite_car(request, pk):
    if request.method == "POST":
        car = car_list.objects.filter(name=request.POST["name"])
        car_detail = car.values('name_detail').distinct().order_by('name_detail')[int(request.POST["name_detail"])]
        
        # 사용자 데이터가 존재하는경우
        if Mypage.objects.filter(author_id = pk):
            
            favorite_car = Mypage.objects.get(author_id=pk)

            favorite_car.favorite_car = car_detail['name_detail']
            favorite_car.save()
            return mypage(request, pk)
            
        # 사용자 데이터가 없는경우
        else:
            user_id = User.objects.get(pk=pk)

            Mypage.objects.create(author=user_id, favorite_car=car_detail['name_detail'])
            return mypage(request, pk)