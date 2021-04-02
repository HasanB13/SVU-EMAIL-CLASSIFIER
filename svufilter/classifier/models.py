from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Messages(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    date_get = models.DateTimeField()
    typeEmail = models.CharField(max_length=20)
    sender = models.CharField(max_length=150)
    reciever = models.ForeignKey(User,on_delete = models.CASCADE)
    def __str__(self):
        return self.subject