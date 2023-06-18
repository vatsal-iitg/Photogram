from django.db import models
from django.utils import timezone # timezone imported
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    body = models.TextField() # left it as textbody currently, will update to Pictures and Captions later 
    created_on = models.DateTimeField(default=timezone.now) # timestamp
    author = models.ForeignKey(User,on_delete=models.CASCADE) # which user owns the post

    class Meta:
        app_label='socialfeed' # for mentioning inside INSTALLED_APPS


class Comment(models.Model):
    comment = models.TextField()
    created_on  = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE) # connected to the user who "comments on" the post
    post=  models.ForeignKey('Post',on_delete=models.CASCADE)
    # connected to the user who "owns" the post
    