from rest_framework import serializers
from .models import *

from django.utils import timezone

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        extra_kwargs = {
            'name': {'read_only': True}
        }

# class Update_profie(serializers.Serializer):
#     name = serializers.CharField(required = False,)
#     bank_name = models.CharField(max_length=100)
#     acc_no =  models.BigIntegerField()
#     ifsc_code = models.CharField(max_length=15)
#     holder_name = models.CharField(max_length=100)
#     mobile = models.BigIntegerField()
#     branch = models.CharField(max_length=100)
        

class LeaveSummarySerializer(serializers.Serializer):
    taken = serializers.IntegerField()
    sick_taken = serializers.IntegerField()
    casual_taken = serializers.IntegerField()
    casual_remaining=serializers.IntegerField()
    sick_remaining = serializers.IntegerField()
    remaining = serializers.IntegerField()
    lop = serializers.IntegerField()



class Attendence_status(serializers.Serializer):
    status = serializers.CharField()
    checkin = serializers.DateTimeField()
    
    
    
    
    
       
     
class Employee_bank_details_serializer(serializers.ModelSerializer):
    class Meta:
        model =Employee_Bank_details
        fields = '__all__'

class Employee_other_details_serializer(serializers.ModelSerializer):
    class Meta:
        model =Employee_other_details
        fields = '__all__'
        

class Employee_documents_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_main_files
        fields = '__all__'
        read_only_fields = ['employee']
        
class Employee_statuory_details_serializer(serializers.ModelSerializer):
    class Meta:
        model =Employee_statuory_information
        fields = '__all__'
        

class Employee_dashboard(serializers.ModelSerializer):
    other_details = Employee_other_details_serializer(source='employee_other_details_set', many=True)
    bank_details = Employee_bank_details_serializer(source='employee_bank_details_set', many=True)
    statutory_details = Employee_statuory_details_serializer(source='employee_statuory_information_set', many=True)

    class Meta:
        model = Employee_Registration
        fields = '__all__'
        
        
class Employee_attendence_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_attendence_details
        fields = '__all__'

class Admin_Employee_dashboard(serializers.ModelSerializer):
    other_details = Employee_other_details_serializer(source='employee_other_details_set', many=True)
    bank_details = Employee_bank_details_serializer(source='employee_bank_details_set', many=True)
    statutory_details = Employee_statuory_details_serializer(source='employee_statuory_information_set', many=True)
    attendence_details = Employee_attendence_serializer(source = 'employee_attendence_details_set',many =True)
    class Meta:
        model = Employee_Registration
        fields = '__all__'   
    
    

 
class Employee_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Registration
        fields = '__all__'
        

class Employee_attendence_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_attendence_details
        fields = '__all__'



class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
class AssetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRequest
        fields = "__all__"

class ReturnAssetSerializers(serializers.ModelSerializer):
    class Meta:
        model=ReturnAsset
        fields="__all__"

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'
    
    
class Employee_main_files_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_main_files
        fields = '__all__'

# class Admin_employee_details(serializers.ModelSerializer):
#     other_details = Employee_other_details_serializer(source='employee_other_details_set', many=True)
#     bank_details = Employee_bank_details_serializer(source='employee_bank_details_set', many=True)
#     statutory_details = Employee_statuory_details_serializer(source='employee_statuory_information_set', many=True)
#     payslip_details = PayslipSerializer(source='payslip_set',many = True)
#     attendence_details = Employee_attendence_serializer(source = 'employee_attendence_set',many=True)
#     class Meta:
#         model = Employee_Registration
#         fields = '__all__'
    
    
class EmployeeCheckInSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Employee_attendence_details
        fields = ['id','data', 'name', 'checkin','checkout'] 
    def create(self, validated_data):
        # Set checkin as current time
        validated_data['checkin'] = timezone.now()
        # Ensure checkout is not saved yet
        validated_data['checkout'] = None
        return super().create(validated_data)



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

class AttendanceRequestSerializer(serializers.ModelSerializer):
    # Fetch the name so we can show it in the Admin Table
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = AttendanceRequest
        fields = '__all__'

class EmployeeBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Break_details
        fields = '__all__'

