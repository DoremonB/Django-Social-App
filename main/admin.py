from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(OneToOneProfile)

