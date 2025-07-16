from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Email Address Not Valid")) 

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser",False)

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        else:
            raise ValueError(_("A Valid Email Address Must Be Provided For This Account"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("An Admin Status Must Be True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser Must Have is_superuser=True")
        return self.create_user(email, password, **extra_fields)          