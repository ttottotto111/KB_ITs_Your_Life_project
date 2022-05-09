from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    path('login/', views.login_screen, name='login_screen'),
    path('create_user/', views.userid_check, name='create_user'),
]