from django.contrib import admin

from .models import Student,OTP,Profile,Post,Followerscount,Like_post,Comment,CustomUser
# Register your models here.
admin.site.register(Student)
admin.site.register(CustomUser)
admin.site.register(OTP)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Followerscount)
admin.site.register(Like_post)
admin.site.register(Comment)