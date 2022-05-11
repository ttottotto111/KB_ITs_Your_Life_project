from django.db import models

# Create your models here.
class maker_test(models.Model):
    maker = models.CharField(max_length=10)