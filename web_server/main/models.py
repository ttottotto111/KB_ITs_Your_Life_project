from pyexpat import model
from django.db import models

# Create your models here.
class car_list_test(models.Model):
    maker = models.CharField(max_length=10)
    car_list = models.CharField(max_length=50)
    def __str__(self):
        return self.maker, self.car_list
    
class car_list(models.Model):
    company = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    name_detail = models.CharField(max_length=50)
    price = models.IntegerField()
    boost = models.IntegerField()
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    km = models.IntegerField()
    change = models.CharField(max_length=10)
    fure = models.CharField(max_length=10)
    find = models.CharField(max_length=10)
    still = models.IntegerField()
    wheel = models.CharField(max_length=10)
    acc = models.IntegerField()
    distroy = models.IntegerField()
    made = models.CharField(max_length=10)
    new_price = models.IntegerField()
    down_rate = models.FloatField()
    rate_year = models.IntegerField(null=True)
    rate_2023 = models.IntegerField(null=True)
    rate_2024 = models.IntegerField(null=True)
    rate_2025 = models.IntegerField(null=True)
    rate_2026 = models.IntegerField(null=True)
    rate_2027 = models.IntegerField(null=True)
    rate_2028 = models.IntegerField(null=True)
    rate_2029 = models.IntegerField(null=True)
    rate_2030 = models.IntegerField(null=True)