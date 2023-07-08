from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,primary_key = True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/',blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    location = models.CharField(max_length=100, blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    

    # followers and following
    followers = models.ManyToManyField(User,blank=True,related_name='followers')
    
    def __str__(self):
        return self.user.get_full_name()
    