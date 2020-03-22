from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    #image_url=models.URLField(max_length=300)
    image_url=models.ImageField(upload_to='images/') 
    caption=models.TextField()
    date_time=models.DateTimeField(auto_now_add=True)
    fk_user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_type=models.IntegerField(default=0)
    like_count=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)


class Comments(models.Model):
    content=models.TextField()
    image_url=models.ImageField(upload_to='images/',null=True, blank=True) 
    date_time=models.DateTimeField(auto_now_add=True)
    fk_user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    fk_post_id=models.ForeignKey(Post,on_delete=models.CASCADE)

class Profile(models.Model):
    fk_user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    display_name=models.CharField(max_length=100,blank=False)
    bio=models.TextField()
    dob=models.DateField()
    image_url=models.URLField(max_length=300)
    
    friends=models.ManyToManyField(User,related_name='friends',blank=True)

class Likes(models.Model):
    fk_user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    fk_post_id=models.ForeignKey(Post,on_delete=models.CASCADE,default=None)
    fk_comments_id=models.ForeignKey(Comments,on_delete=models.CASCADE,blank=True, null=True)

class Notification(models.Model):
    notif_type=models.IntegerField(default=0)
    fk_sender_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="fk_sender_id")
    fk_receiver_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="fk_receiver_id")
    fk_post_id=models.ForeignKey(Post,on_delete=models.CASCADE,null=True, blank=True)
    content=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)

class OneToOneProfile(models.Model):
    fk_user_id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    display_name=models.CharField(max_length=100,blank=False)
    bio=models.TextField()
    dob=models.DateField()
    image_url=models.ImageField(upload_to='images/') 

    Friends=models.ManyToManyField(User,related_name='Friends',blank=True)
