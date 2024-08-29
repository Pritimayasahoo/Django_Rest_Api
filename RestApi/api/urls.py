from django.urls import path
from .views import studentapi,get_csrf_token

urlpatterns = [
   path('csrf/',get_csrf_token),
   path('student/<int:pk>',studentapi) 
]
