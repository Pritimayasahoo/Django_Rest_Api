from django.urls import path
from .views import studentapi,get_csrf_token,signup_view
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
   path('csrf/',get_csrf_token),
   path('student/<int:pk>',studentapi) ,
   path('signup/', signup_view, name='signup'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
