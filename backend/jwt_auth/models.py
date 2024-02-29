from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
