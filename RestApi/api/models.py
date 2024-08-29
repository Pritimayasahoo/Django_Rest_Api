from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=20)
    rool=models.IntegerField()
    section=models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.name 
