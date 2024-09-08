from django.urls import path
from .views import studentapi,get_csrf_token,signup_view,login_view,forgotpassword,forgot_otp_check
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
   path('csrf/',get_csrf_token),
   path('student/<int:pk>',studentapi) ,
   path('signup/', signup_view, name='signup'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   path('login/', login_view, name='login'),
   path('passwordreset/',forgotpassword,name='forgotpassword'),
   path('otpcheck/',forgot_otp_check,name='otpcheck')
]
