
from os import access
from django.db import models
from django.contrib.auth.models import (BaseUserManager, PermissionsMixin, AbstractBaseUser)
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError("Users should have username")
        if email is None:
            raise TypeError("Users should have a Email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):

        if password is None:
            raise TypeError("Password should not be None")
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified=models.BooleanField(default=True)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # define the attributes the user will be using to login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # how to manage the objects of the user

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access': str(refresh.access_token)
            }

 

