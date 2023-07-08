from django.contrib import admin
from .models import Post,UserProfile,Comment,Message

# Register your models here.
admin.site.register(Post)

admin.site.register(Comment)


# registered user profile
admin.site.register(UserProfile) 
admin.site.register(Message) 
