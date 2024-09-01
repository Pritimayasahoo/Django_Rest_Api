from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

# Create your models here.

'''Use AbstractUser to modfy the default user model and add new fields (use AbstractBaseUser to create admin model from scracth)'''

class CustomUser(AbstractUser):
    #username=None --> Not use default username for login
    username = None
    email = models.EmailField(unique=True)
    #USERNAME_FIELD = 'email' --> email as the default field to create user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    #use the CustomUserManager for create custom user
    objects = CustomUserManager()


class Student(models.Model):
    name=models.CharField(max_length=20)
    rool=models.IntegerField()
    section=models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.name 
