from django.db import models

# Create your models here.
class User_Info(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    pwd = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)