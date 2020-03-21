from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import *

class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def save(self,commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        else:
            return User

from django.forms import ModelForm
class ProfileForm(ModelForm):
    # display_name=forms.CharField(max_length=100,label='name')
    # bio=forms.CharField(max_length=100,label='bio')
    # dob=forms.DateField(label='dob')
    # image_url=forms.URLField(label='image_url')
    class Meta:
        model=OneToOneProfile
        fields=['display_name','bio','dob','image_url']


class PostForm(ModelForm):
    #image_url=forms.URLField(max_length=300)
    #caption=forms.CharField(max_length=100)

    class Meta:
        model=Post
        fields=['image_url','caption']

class CommentForm(ModelForm):

    class Meta:
        model=Comments
        fields=['content','image_url']

