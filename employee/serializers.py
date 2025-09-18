from rest_framework import serializers
from .models import Employee, DynamicField

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'dynamic_data']
