from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None  # 이메일 로그인 쓸거기 때문에

    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
