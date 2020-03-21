from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('base/', views.base,name='name_base'),
    path('home/', views.home,name='name_home'),
    path('register/', views.register,name='name_register'),
    path('login/', views.view_login,name='name_login'),
    path('logout/', views.view_logout,name='name_logout'),
    path('set_profile/',views.set_profile,name='name_set_profile'),
    path('get_profile/<int:pk>',views.get_profile,name='name_get_profile'),
    path('put_post/<int:posttype>',views.put_post,name='name_put_post'),
    # path('landing_page/', views.landing_page,name='name_landing'),
    path('view_all_users/',views.view_all_users,name='name_view_all_users'),
    path('view_my_friends/',views.view_my_friends,name='name_view_my_friends'),
    path('like/<int:pk>',views.like,name='name_like'),
    path('show_like/<int:pk>',views.show_like,name='name_show_like'),

    path('add_friend/<int:pk>',views.add_friend,name='name_add_friend'),
    path('remove_friend/<int:pk>',views.remove_friend,name='name_remove_friend'),
    path('notifications/',views.notifications,name='name_notifications'),
    path('display_single_post/<int:pk>',views.display_single_post,name='name_display_single_post'),
    
    #path('add_comment/<int:postId>',views.add_comment,name='name_add_comment'),
    path('delete_nofitication/<int:pk>',views.delete_notification,name='name_delete_notification'),

    path('like/', views.like, name='like')
    
]
