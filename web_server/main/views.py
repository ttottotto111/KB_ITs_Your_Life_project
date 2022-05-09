from django.shortcuts import render, redirect
from blog.models import Post
from .models import User_Info
import datetime

# Create your views here.
def main(request):
    posts = Post.objects.all().order_by('-pk')
    
    return render(request,"main/main.html",
                  {
                      'posts':posts
                  })

# 로그인화면
def login_screen(request):
    return render(request, "main/login_screen.html")

# 중복아이디 체크
def userid_check(request):       
    if request.method == 'POST':
        post_data = request.POST
        try:
            User_Info.objects.get(id = post_data.get('id'))
            return render(request, "main/create_user.html",
                          {"id":post_data.get('id')})
        except:
            data = User_Info(
                id = post_data.get('id'),
                pwd = post_data.get('pwd'),
                created_at = datetime.datetime.now()
            )
            data.save()
            return redirect('login_screen')
    return render(request, "main/create_user.html")
        
# 회원가입 화면
def create_user(request):
    try:
        if request.method == 'POST':  
            post_data = request.POST
            
            #비밀번호 미입력시
            if post_data.get('pwd')=="":
                return render(request, "main/create_user.html",
                      {
                          "id": "비밀번호를 입력하세요."
                      })
            
            data = User_Info(
                    id = post_data.get('id'),
                    pwd = post_data.get('pwd'),
                    created_at = datetime.datetime.now()
                )
            data.save()
            return redirect('login_screen')
        return render(request, "main/create_user.html")
            #return render(request, "main/create_user.html")
    except:
        post_data = request.POST
        return render(request, "main/create_user.html",
                      {
                          "id": post_data.get("id")+" : 중복된 아이디입니다."
                      })