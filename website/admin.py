from django.contrib import admin
from .models import Records
from user.models import OtpToken

# Register your models here.
admin.site.register(Records)
admin.site.register(OtpToken)
