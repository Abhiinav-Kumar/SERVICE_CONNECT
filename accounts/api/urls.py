from django.urls import path
from accounts.api.views import UsersListAV,RegisterUsersAV,LoginUserAV,VerifyOtpAV,ProfileAV,LogoutViewAV
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/',UsersListAV.as_view(),name='users-list'),
    path('register/',RegisterUsersAV.as_view(),name='register'),
    path('login/',LoginUserAV.as_view(),name='login'),
    path('login/otp-verify/',VerifyOtpAV.as_view(),name='otp-verify'),
    path('logout/',LogoutViewAV.as_view(), name='logout'),
    
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    
    path('profile/',ProfileAV.as_view(), name='profile-creation'),
    
    
    
    
]