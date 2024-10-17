from rest_framework import serializers
from .models import Student,OTP,Profile,Post,Followerscount,Like_post,Comment,CustomUser


class Studentserializer(serializers.ModelSerializer):
   class Meta:
       model=Student
       fields=['name','rool','section']

class OTPserializer(serializers.ModelSerializer):
    class Meta:
        model=OTP
        fields=all

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=all

class Postserializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=all                

class Followerscountserializer(serializers.ModelSerializer):
    class Meta:
        model=Followerscount
        fields=all

class Like_postserializer(serializers.ModelSerializer):
    class Meta:
        model=Like_post
        fields=all
   
class Commentserializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=all

class CustomUserserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=all
                                