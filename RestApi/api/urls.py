from django.urls import path
from .views import studentapi

urlpatterns = [
   path('student/<int:pk>',studentapi) 
]
