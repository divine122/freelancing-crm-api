from django.db import models
from django.utils.translation  import gettext_lazy as _
from django.contrib.auh.models import AbstractBaseUser,PermissionMixin
from django.core.validators import MinLengthValidator
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number(models.CharField(max_length=15,validators=[MinLengthValidator(11)]))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login date"), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()
    def __str__(self):
        return f"{self.email}"
