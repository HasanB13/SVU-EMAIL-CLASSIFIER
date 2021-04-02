from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class mailModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    password = models.CharField(max_length=10000)