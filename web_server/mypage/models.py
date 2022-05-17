from django.db import models
from django.contrib.auth.models import User
from pandas import notnull

# Create your models here.

class Mypage(models.Model):
    #사용자 id
    author = models.OneToOneField(User, on_delete = models.CASCADE)
    #자기소개
    content = models.TextField(max_length=100, null=True)
    #프로필 이미지
    profile_img = models.ImageField(upload_to='mypage/images/%Y/%m/%d/',blank=True)