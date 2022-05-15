from django.urls import path, include
from . import views
import blog.views as blog_views

urlpatterns = [
    path('<int:pk>/', views.mypage,name="mypage"),
]