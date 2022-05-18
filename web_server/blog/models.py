from logging import PlaceHolder
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
import os
from main.models import car_list_test
from django import forms

# Create your models here.

class Tag(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=200,unique=True,allow_unicode=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=200, unique=True,allow_unicode=True)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    class Meta:
         verbose_name_plural='Categories'
class car(models.Model):
    name=('general','cookie')
    
    def __str__(self):
        return self.name

class Post(models.Model):
    #car = car_list_test.objects.values('maker').distinct().order_by('maker')
    국산=(('국산','국산'),('해외','해외'))
    구동방식=(('4륜 ','4륜 '),('전륜','전륜'),('후륜','후륜'))
    있없=(('없음','없음'),('있음','있음'))
    기름=(('경유 ','경유 '),('LPG','LPG'),('경유+전기','경유+전기'),('하이브리드','하이브리드'),('휘발유','휘발유'))
    캐스=(('캐스퍼','캐스퍼'),('소나타','소나타'))
    종류=(('현대','현대'),('기아', '기아'), ('쉐보레','쉐보레'), ('르노삼성','르노삼성'), ('쌍용','쌍용'), ('제네시스','제네시스'), ('BMW','BMW'), ('벤츠','벤츠'), 
        ('아우디','아우디'),('폭스바겐' ,'폭스바겐'),
        ('미니','미니'), ('지프','지프'), ('포드','포드'),('볼보','볼보'),('랜드로버', '랜드로버'), ('푸조','푸조'),('재규어', '재규어'), ('렉서스','렉서스'), ('링컨','링컨'), 
        ('인피니티','인피니티'), ('혼다','혼다'),
        ('도요타','도요타'),('포르쉐' ,'포르쉐'),('닛산', '닛산'), ('캐딜락','캐딜락'),('대형트럭(2톤이상)', '대형트럭(2톤이상)'),('마세라티', '마세라티'),
        ('시트로엥','시트로엥'),('토요타','토요타'), ('크라이슬러','크라이슬러'),
        ('피아트','피아트'), ('대형버스(16인승이상)','대형버스(16인승이상)'), ('테슬라','테슬라'), ('닷지','닷지'), ('미쯔비시','미쯔비시'), ('북기은상','북기은상'), 
        ( '스마트','스마트'), ('벤틀리','벤틀리'),
        ( '애스턴마틴','애스턴마틴'),( '롤스로이스','롤스로이스'), ('선롱','선롱'), ('람보르기니','람보르기니'),('험머', '험머'))
    
    브랜드= models.CharField(max_length=30,blank=True,null=True,choices=종류)
    차종 = models.CharField(max_length=50,blank=True,null=True)
    가격=models.CharField(max_length=100,blank=True)
    연식 = models.CharField(max_length=30,blank=True)
    주행거리 = models.CharField(max_length=30,blank=True)
    연료 = models.CharField(max_length=30,blank=True,choices=기름)
    구동방식 = models.CharField(max_length=30,blank=True,choices=구동방식)
    연비 = models.CharField(max_length=30,blank=True)
    배기량 = models.CharField(max_length=30,blank=True)
    색상 = models.CharField(max_length=30,blank=True)
    사고유무 = models.CharField(max_length=30,blank=True,choices=있없)
    압류및저당 = models.CharField(max_length=30,blank=True,choices=있없)
    전속이력 = models.CharField(max_length=30,blank=True,choices=있없)
    차사진 =models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True)
    file_upload=models.FileField(upload_to='blog/files/%Y/%m/%d/',blank=True)
    내용 = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    category=models.ForeignKey(Category,null=True,blank=True, on_delete=models.SET_NULL)
    생산지= models.CharField(max_length=5,blank=True,choices=국산)
    #tags=models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'
    


    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    def get_user_url(self):
        return f'/mypage/{self.author.id}'
    


    

    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/963/5e19b90b4ef21a68/svg/{self.author.email}'
        
    def get_mypage_url(self):
        return f'/blog/{self.post_id}'