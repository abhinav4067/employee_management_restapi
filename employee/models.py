from django.db import models

# Create your models here.
from django.db import models
from emp_admin.models import *
# Create your models 
class Employee(models.Model):
    dynamic_data = models.JSONField()  # Everything, including 'Name', goes here

    def __str__(self):
        return self.dynamic_data.get('Name', 'Employee')
