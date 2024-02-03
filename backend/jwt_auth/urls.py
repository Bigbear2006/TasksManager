from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

from . import views

urlpatterns = [
    path('register-user/', views.RegisterUserAPIView.as_view(), name='register-user'),
    path('register-admin/', views.RegisterAdminAPIView.as_view(), name='register-admin'),
    path('user-info/', views.UserInfoAPIView.as_view(), name='user-info'),
    path('get-token/', token_obtain_pair, name='get-token'),
    path('refresh-token/', token_refresh, name='refresh-token'),
    path('verify-token/', token_verify, name='verify-token'),
]
