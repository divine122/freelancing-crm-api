from django.db import models

# Create your models here.
class Records(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=222)
    state = models.CharField(max_length=222)
    zipcode = models.CharField(max_length=445)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")