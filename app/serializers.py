from rest_framework import serializers
from .models import Employee_Registration

class Employee_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Registration
        fields = '__all__'
