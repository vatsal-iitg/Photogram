from django.db import models
from django.utils import timezone # timezone imported
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
from django.forms import DateTimeField


# Create your models here.
class Post(models.Model):
    body = models.TextField()

    # added image field 
    image = models.ImageField(upload_to='post_photos',blank=True, null=True)

    created_on = models.DateTimeField(default=timezone.now) 
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    # added likes and dislikes field
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name='dislikes')

    class Meta:
        app_label='socialfeed' # for mentioning inside INSTALLED_APPS


class Comment(models.Model):
    comment = models.TextField()
    created_on  = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE) # connected to the user who "comments on" the post
    post=  models.ForeignKey('Post',on_delete=models.CASCADE)
    # connected to the user who "owns" the post



    # added likes and dislikes field
    likes = models.ManyToManyField(User,blank=True,related_name="comment_likes")
    dislikes = models.ManyToManyField(User,blank=True,related_name="comment_dislikes")

    # parent commments are those which are made to the original posts and not replies to comments
    # children comments are those which are added as replies to other comments
    parent = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True,related_name='+')


    # these are two functions 
    # children function returns the children comments of a parent comment
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    # parent function returns the children comments of a parent comment
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class UserProfile(models.Model):
    user = models.OneToOneField(User,primary_key=True,verbose_name='user',related_name='profile',on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/profile_pics',default='avatar/profile_pics/default.png',)
    name= models.CharField(max_length=30,blank=True,null=True)
    bio = models.TextField(max_length=500,blank=True,null=True)
    date_of_birth = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=100,blank=True,null=True)    
    followers = models.ManyToManyField(User,related_name='followers',blank=True)

# creating profile as the user is created
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save() 


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def sender_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        sender_message.save()
    
        reciepient_message = Message(
            user=to_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        reciepient_message.save()
        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users
