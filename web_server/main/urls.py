from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('accounts/', include('allauth.urls')),
    path('', views.car_maker, name="car_maker")
]