from django.urls import path, include
from . import views
import blog.views as blog_views

urlpatterns = [
    path('<int:pk>/', views.mypage,name="mypage"),
    path('user_img/<int:pk>', views.user_img, name="user_img"),
    path('user_content/<int:pk>', views.user_content, name="user_content"),
    path('favorite_car/<int:pk>', views.favorite_car, name="favorite_car"),
    path('car_list/<str:maker>/', views.car_name, name="car_name"),
    path('car_detail/<str:car>/', views.car_detail, name="car_detail"),
]