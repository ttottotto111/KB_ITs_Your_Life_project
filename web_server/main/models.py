from pyexpat import model
from django.db import models

# Create your models here.
class car_list_test(models.Model):
    maker = models.CharField(max_length=10)
    car_list = models.CharField(max_length=50)
    def __str__(self):
        return self.maker, self.car_list