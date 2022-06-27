from django.urls import path, include
from . import views

urlpatterns = [
    #메인 화면
    path('', views.main, name="main"),
    
    #로그인 했을경우 게시물 변경
    path('user_id/<int:id>', views.login_main, name="login_name"),
    
    # 구글 로그인
    path('accounts/', include('allauth.urls')),
    
    # 회사명으로 차종 검색
    path('<str:pk>', views.car_maker, name="car_maker"),
    
    # 차종으로 세부차종 검색
    path('car_detail/<str:car_name>', views.car_detail, name="car_detail"),
    
    # 그래프 데이터 전송
    path('car_chart/<str:car_name>/<int:detail_no>', views.car_chart, name="car_chart"),
]