from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
    path('csrf/',views.get_csrf_token),
    path('student/<int:pk>',views.studentapi) ,
    path('signup/',views.signup_view, name='signup'),
    path('token/refresh/',views.refresh_token, name='token_refresh'),
    path('token/verify/',views.verify_token, name='token_verify'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('passwordreset/',views.forgotpassword,name='forgotpassword'),
    path('otpcheck/',views.forgot_otp_check,name='otpcheck'),
    path('profile/',views.create_profile,name='profile'),
    path('view_profile/<str:name>',views.view_profile,name='post'),
    path('follow/',views.Follow,name='follow'),
    path('like/',views.like_check,name='like'),
    path('search/',views.Search,name='search'),
    path('prof/',views.Own_profile,name='own_profile'),
    path('showcomment/',views.Showcomment,name='showcomment'),
    path('createcomment/',views.Createcomment,name='createcomment'),
    path('save/',views.handle_compressed_image,name='save_post'),
    path('editprof/',views.Own_edit_profile,name='own_edit_profile'),
    path('deletepic/',views.Deletepic,name='Deletepic'),
    path('forgot/',views.forgotpassword,name='forgot'),
    path('forgot_otp/',views.forgot_otp_check,name='forgot_otp'),
]
