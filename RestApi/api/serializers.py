from rest_framework import serializers
from .models import Student,OTP,Profile,Post,Followerscount,Like_post,Comment,CustomUser


class Studentserializer(serializers.ModelSerializer):
   class Meta:
       model=Student
       fields=['name','rool','section']

class OTPserializer(serializers.ModelSerializer):
    class Meta:
        model=OTP
        fields='__all__'

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = '__all__'

class Postserializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = '__all__'                

class Followerscountserializer(serializers.ModelSerializer):
    class Meta:
        model=Followerscount
        fields = '__all__'

class Like_postserializer(serializers.ModelSerializer):
    class Meta:
        model=Like_post
        fields = '__all__'
   
class Commentserializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = '__all__'

class CustomUserserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = '__all__'
                                