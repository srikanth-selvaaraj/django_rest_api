from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("Email required")

        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model, created with AbstractBaseUser
    with built-in permissions
    """
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
