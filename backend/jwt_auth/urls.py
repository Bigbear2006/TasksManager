from django.urls import path
from rest_framework_simplejwt.views import token_refresh, token_obtain_pair, token_verify

from . import views

urlpatterns = [
    path('register-user/', views.RegisterUserAPIView.as_view(), name='register-user'),
    path('verify-email/', views.VerifyEmailAPIView.as_view(), name='verify-email'),
    path('user-info/', views.UserInfoAPIView.as_view(), name='user-info'),
    path('users/', views.UsersListAPIView.as_view(), name='users-list'),
    path('send-email-again/', views.SendEmailAgain.as_view(), name='send-email-again'),

    path('get-token/', token_obtain_pair, name='get-token'),
    path('refresh-token/', token_refresh, name='refresh-token'),
    path('verify-token/', token_verify, name='verify-token'),
]
