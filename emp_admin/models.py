from django.db import models

# Create your models here.
# emp_admin/models.py
from django.db import models


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username



class DynamicField(models.Model):
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50)  # text, number, date, password

    def __str__(self):
        return f"{self.label} ({self.field_type})"
