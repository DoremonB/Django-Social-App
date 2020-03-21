from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def home(request):

    try:
        profile=OneToOneProfile.objects.filter(fk_user_id=request.user)[0]
        #friend_list=profile.friends.all().values_list('id', flat=True)
        friend_list=profile.Friends.all()
        print(friend_list)
        # li=[]
        # for i in range(len(friend_list)):
        #     li.append(friend_list[i])
        # print(li)
        
        posts=Post.objects.filter(fk_user_id__in=friend_list).order_by("-date_time")
        print(posts)

        return render(request,'main/home.html',{'posts':posts})

    except Exception as identifier:
        print(identifier)
        posts=Post.objects.filter(fk_user_id=99)
        name="You have no friends yet :)"
        return render(request,'main/home.html',{'posts':posts,'name':name})
    


def base(request):
    return render(request,'main/base.html')

#working
def register(request):
    print('Here')
    if request.method=='POST':
        print('Here2')
        form=NewUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            
            form.save()
            return redirect('name_login')
        else:
            print(f'Error')
            return redirect('name_register')

    else:
        form=NewUserForm()
        return render(request,'main/register.html',context={"form":form})

#working
def view_login(request):
    form=AuthenticationForm
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(f'{username} {password}')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('name_home')
            else:
                return render(request,'main/login.html',{'form':form})
        else:
            print('Wrong form')
            return redirect('name_login')
    
    
    return render(request,'main/login.html',{"form":form})

#working
def view_logout(request):
    logout(request)
    return redirect("name_home")

@login_required
def set_profile(request):
    form=ProfileForm
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            # display_name=form.cleaned_data['display_name']
            # bio=form.cleaned_data['bio']
            # dob=form.cleaned_data['dob']
            # image_url=form.cleaned_data['image_url']
            
            #changed
            #pr=OneToOneProfile(fk_user_id=user,display_name=display_name,bio=bio,dob=dob,image_url=image_url)
            #pr.save()

            temp_form=form.save(commit=False)
            temp_form.fk_user_id=request.user
            temp_form.save()
            url='http://127.0.0.1:8000/main/get_profile/'+str(request.user.pk)
            print(url)
            return redirect(url)
        else:
            return render(request,'main/profile.html',{'form':form})
    return render(request,'main/profile.html',{'form':form})


@login_required
def get_profile(request,pk):
    profile=OneToOneProfile.objects.filter(fk_user_id=pk)[0] 
    
    name=profile.display_name
    bio=profile.bio
    dob=profile.dob
    image_url=profile.image_url

    posts=Post.objects.filter(fk_user_id=pk)

    return render(request,'main/display_profile.html',{'u':pk,'name':name,'bio':bio,'dob':dob,'image_url':image_url,'posts':posts})

@login_required
def add_friend(request,pk):
    profile=OneToOneProfile.objects.filter(fk_user_id=request.user)[0] 
    requested_user=User.objects.filter(pk=pk)[0]

    profile.Friends.add(requested_user)

    n=Notification(notif_type=2,fk_sender_id=request.user,fk_receiver_id=requested_user,content=f"{request.user} sent you a Friend Request")
    n.save()

    name=profile.display_name
    bio=profile.bio
    dob=profile.dob
    image_url=profile.image_url

    return redirect('name_view_my_friends')

@login_required
def remove_friend(request,pk):
    profile=OneToOneProfile.objects.filter(fk_user_id=request.user)[0] 
    requested_user=User.objects.filter(pk=pk)[0]

    profile.Friends.remove(requested_user)

    Notification.objects.filter(notif_type=2).filter(fk_sender_id=request.user).filter(fk_receiver_id=requested_user).delete()


    name=profile.display_name
    bio=profile.bio
    dob=profile.dob
    image_url=profile.image_url

    return redirect('name_view_my_friends')



@login_required
def put_post(request,posttype):
    form=PostForm
    if request.method=='POST':
        
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            # user=request.user
            # image_url=form.cleaned_data['image_url']
            # caption=form.cleaned_data['caption']
            # # date_time=request.cleaned_data['date_time']
            # fk_user_id=user
            # post_type=posttype

            # p=Post(image_url=image_url,caption=caption,fk_user_id=user,post_type=post_type)
            # p.save()

            image_url=models.ImageField(upload_to='images/') 
    
            temp_form=form.save(commit=False)
            temp_form.fk_user_id=request.user
            temp_form.post_type=1
            temp_form.save()
            

            return redirect('name_home')
        else:
            print('here')
            form=PostForm
            return render(request,'main/post_photo.html',{'form':form})
    return render(request,'main/post_photo.html',{'form':form})

@login_required
def like(request,pk):
    
    p=Post.objects.filter(pk=pk)[0]
    l=Likes.objects.filter(fk_post_id=pk).filter(fk_user_id=request.user)
    print(l)
    if len(l)==0:
        new_l=Likes(fk_user_id=request.user,fk_post_id=p)
        new_l.save()
        curr_like_count=p.like_count
        p.like_count=curr_like_count+1
        p.save()
    else:
        l.delete()
        curr_like_count=p.like_count
        p.like_count=curr_like_count-1
        p.save()
        
    return redirect('name_home')

def show_like(request,pk):
    l=Likes.objects.filter(fk_post_id=pk)
    post=Post.objects.filter(pk=pk)[0]
    return render(request,'main/show_like.html',{'likes':l,"post":post})

@login_required
def view_all_users(request):
    profile=OneToOneProfile.objects.filter(fk_user_id=request.user)[0] 
    context={
        'all_users':User.objects.all(),
        'my_friends':profile.Friends.all()
    }
    return render(request,'main/view_all_users.html',context)

@login_required
def view_my_friends(request):
    profile=OneToOneProfile.objects.filter(fk_user_id=request.user)[0] 
    context={
        'my_friends':profile.Friends.all()
    }
    return render(request,'main/view_my_friends.html',context)

def like(request):
    if request.method == 'GET':
        pk = request.GET['post_id']
        p=Post.objects.filter(pk=pk)[0]
        l=Likes.objects.filter(fk_post_id=pk).filter(fk_user_id=request.user)
        print(l)
        if len(l)==0:
            new_l=Likes(fk_user_id=request.user,fk_post_id=p)
            new_l.save()
            curr_like_count=p.like_count
            p.like_count=curr_like_count+1
            p.save()
            
            print(request.user)
            print(p.fk_user_id)
            n=Notification(fk_sender_id=request.user,fk_receiver_id=p.fk_user_id,fk_post_id=p,content=f"{request.user} liked Post:'{p.caption}'")
            n.save()
            print('like')
        else:
            l.delete()
            curr_like_count=p.like_count
            p.like_count=curr_like_count-1
            p.save()

            Notification.objects.filter(fk_sender_id=request.user).filter(fk_receiver_id=p.fk_user_id).filter(fk_post_id=p).delete()
            print('remove like')
        return HttpResponse(str(p.like_count))
    else:
        return HttpResponse("unsuccesful")

def notifications(request):
    notifs=Notification.objects.filter(fk_receiver_id=request.user).order_by("-date_time")
    return render(request,'main/notifications.html',{'notifs':notifs})

def display_single_post(request,pk):
    post=Post.objects.filter(pk=pk)[0]
    form=CommentForm
    comments=Comments.objects.filter(fk_post_id=pk)
    if request.method=='POST':
        form=CommentForm(request.POST,request.FILES)
        if form.is_valid:
            p=Post.objects.filter(pk=pk)[0]
            temp_form=form.save(commit=False)
            temp_form.fk_user_id=request.user
            temp_form.fk_post_id=p
            temp_form.save()

            n=Notification(notif_type=3,fk_sender_id=request.user,fk_receiver_id=post.fk_user_id,fk_post_id=post,content=f"{request.user} commented on Post:'{p.caption}'")
            n.save()
    else:
        form=CommentForm
        return render(request,'main/display_single_post.html',{'form':form,'post':post,'comments':comments})
    return render(request,'main/display_single_post.html',{'form':form,'post':post,'comments':comments})

def delete_notification(request,pk):
    Notification.objects.filter(pk=pk).delete()
    return redirect('name_notifications')

# def add_comment(request,postId):
#     form=CommentForm
#     if request.method=='POST':
#         form=CommentForm(request.POST,request.FILES)
#         if form.is_valid:
#             p=Post.objects.filter(pk=postId)[0]
#             temp_form=form.save(commit=False)
#             temp_form.fk_user_id=request.user
#             temp_form.fk_post_id=p
#             temp_form.save()
#             return redirect('name_home')

#     else:
#         form=CommentForm
#         return render(request,'main/comment.html',{'form':form})