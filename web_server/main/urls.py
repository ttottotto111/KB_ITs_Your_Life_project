from django.urls import path, include
from . import views

urlpatterns = [
    #메인 화면
    path('', views.main, name="main"),
    
    # 구글 로그인
    path('accounts/', include('allauth.urls')),
    
    # 회사명으로 차종 검색
    path('<str:pk>', views.car_maker, name="car_maker"),
    
]