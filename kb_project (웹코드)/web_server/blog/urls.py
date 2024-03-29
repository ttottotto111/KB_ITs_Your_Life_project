"""sample_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:q>/',views.PostSearch.as_view()),
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
    path('delete_comment/<int:pk>/',views.delete_comment),
    path('create_post/',views.PostCreate.as_view()),
    #path('tag/<str:slug>/',views.tag_page),
    path('category/<str:slug>/',views.category_page),
    path('<int:pk>/',views.PostDetail.as_view()),
    path('',views.PostList.as_view()),
    path('<int:pk>/new_comment/',views.new_comment),
    path('create_post/made/<str:pk>', views.car_maker, name="car_maker"),
    path('create_post/brand/<str:car_name>', views.car_brand, name="car_brand"),
    path('create_post/detail/<str:car_deta>', views.car_detail, name="car_detail"),
    path('create_post/lee/<str:lee>',views.car_lee, name="car_lee"),
    path('create_post/car_picture/',views.car_tensor, name="car_tensor"),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('<int:pk>/remove/',views.remove_post),
    #path('<int:pk>/',views.single_post_page),
    #path('',views.index),
]
