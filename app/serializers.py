from rest_framework import serializers
from .models import Employee_Registration,Employee_attendence

class Employee_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Registration
        fields = '__all__'
        

class Employee_attendence_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_attendence
        fields = '__all__'
        


from django.utils import timezone

class EmployeeCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_attendence
        fields = ['id', 'name', 'checkin']
        
        
    def create(self, validated_data):
        # Set checkin as current time
        validated_data['checkin'] = timezone.now()
        # Ensure checkout is not saved yet
        validated_data['checkout'] = None
        return super().create(validated_data)



from rest_framework import serializers
from .models import Employee_Registration


class EmployeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            employee = Employee_Registration.objects.get(email=email, password=password)
        except Employee_Registration.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        data['employee'] = employee
        return data
