from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, User
)
from django.urls import reverse_lazy


# class UserManager(BaseUserManager):
#     ''' ユーザマネージャモデル '''

#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Emailを入力してください")
#         if not username:
#             raise ValueError("ユーザー名を入力してください")
#         user = self.model(
#             username=username,
#             email=email
#         )
#         user.set_password(password)
#         user.save(using=self._db)  # DBに保存
#         return user
    
    
#     def create_superuser(self, username, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, email, password, **extra_fields)


# class Users(AbstractBaseUser, PermissionsMixin):
#     ''' ユーザモデル '''
#     username = models.CharField(max_length=150,unique=True)
#     email = models.EmailField(max_length=255,unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]
#     objects = UserManager()

#     def get_absolute_url(self):
#         return reverse_lazy("accounts:home")