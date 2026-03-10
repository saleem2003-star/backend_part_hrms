from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET','POST'])
def employee_data(request):
    if request.method == 'GET':
        employees = Employee_Registration.objects.all()
        serializer = Employee_serializer(employees, many=True)
        return Response(serializer.data)
    print(employees)
    
@csrf_exempt
@api_view(['GET','POST'])
def create_data(request):
    if request.method == 'POST':
        print("POST request received")
        print("Raw request data:", request.data)
        serializer = Employee_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("Saved data:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        
@csrf_exempt
@api_view(['POST'])
def employee_login(request):
    serializer = EmployeeLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    employee = serializer.validated_data['employee'] 
    emp_serializer = Employee_serializer(employee) 
    return Response({
        "status": "success",
        "message":"invalid password or email",
        "employee_data": emp_serializer.data
    }) 
    

@csrf_exempt
@api_view(['GET','POST'])
def employee_attendence(request):
    if request.method == 'GET':
        employees = Employee_attendence_details.objects.all()
        serializer = Employee_attendence_serializer(employees, many=True)
        return Response(serializer.data)
    print(employees)



        
# @csrf_exempt
# @api_view(['GET','POST'])
# def employee_attendence_create(request):
#     employee_id = request.data.get('id')
#     print(employee_id)
#     if not employee_id:
#         return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         employee = Employee_Registration.objects.get(id=employee_id)
#     except Employee_Registration.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
#     attendance = Employee_attendence.objects.create(
#         name=employee,
#         checkin=timezone.now()
#     )

#     serializer = Employee_attendence_serializer(attendance)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)




# # @api_view(['PUT'])
# # def attendence_logout(request):
# #     if request.method == 'PUT':
# #         employee_id = request.data.get('id')
# #         employee = Employee_Registration.objects.get(id=employee_id)
# #         attendence = Employee_attendence.objects.filter(name = employee,checkout__isnull = True)
# #         attendence.checkout = timezone.now()
# #         attendence.save(update_fields=['checkout'])
# # from django.utils import timezone
# # from rest_framework.response import Response
# # from rest_framework import status


# @csrf_exempt
# @api_view(['PUT'])
# def attendence_logout(request):
#     employee_id = request.data.get('id')
#     if not employee_id:
#         return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         employee = Employee_Registration.objects.get(id=employee_id)
#     except Employee_Registration.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
#     attendance = Employee_attendence.objects.filter(
#         name=employee,
#         checkout__isnull=True
#     ).order_by('-checkin').first()
#     if not attendance:
#         return Response({"error": "No active punch-in found"}, status=status.HTTP_400_BAD_REQUEST)
#     attendance.checkout = timezone.now()
#     attendance.save(update_fields=['checkout'])
#     return Response({"message": "Checkout updated successfully"}, status=status.HTTP_200_OK)
       
       
@csrf_exempt
@api_view(['POST'])
def employee_attendence_create(request):
    employee_id = request.data.get('id')
    if not employee_id:
        return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        employee = Employee_Registration.objects.get(id=employee_id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    today = timezone.localdate()
    attendance = Employee_attendence_details.objects.filter(name=employee, date=today).first()
    if attendance:
        return Response({"error": "Already punched in today"}, status=status.HTTP_400_BAD_REQUEST)
    attendance = Employee_attendence_details.objects.create(
        name=employee,
        date=today,
        checkin=timezone.now()
    )
    serializer = Employee_attendence_serializer(attendance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['PUT'])
def attendence_logout(request):
    employee_id = request.data.get('id')
    if not employee_id:
        return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        employee = Employee_Registration.objects.get(id=employee_id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    today = timezone.localdate()
    attendance = Employee_attendence_details.objects.filter(
        name=employee,
        date=today,
        checkout__isnull=True
    ).first()

    if not attendance:
        return Response({"error": "No active punch-in found for today"}, status=status.HTTP_400_BAD_REQUEST)

    attendance.checkout = timezone.now()
    attendance.save(update_fields=['checkout'])
    return Response({"message": "Checkout updated successfully"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET','POST'])
def employee_dashboard(request,id):
    employee = Employee_Registration.objects.get(id=id)
    serializer = Employee_dashboard(employee)
    return Response(serializer.data)



@csrf_exempt
@api_view(['GET','POST'])
def admin_employee(request,id):
     employee = Employee_Registration.objects.get(id=id)
     serializer = Admin_Employee_dashboard(employee)
     return Response(serializer.data)
# @csrf_exempt
# @api_view(['GET','POST'])
# def admin_employee_details(request,id):
#     employee = Employee_Registration.objects.get(id=id)
#     serializer = Admin_employee_details(employee)
#     print(serializer.errors)
#     return Response(serializer.data)

# def apply_leave(request,id):

#     Leave.objects.filter(
#         created_at__lt=timezone.now() - timedelta(days=60)
#     ).delete()

#     if request.method == 'GET':
#         leaves = Leave.objects.all().order_by('-id')
#         serializer = LeaveSerializer(leaves, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = LeaveSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Leave applied Successfully"})
#         return Response(serializer.errors, status=400)
@csrf_exempt
@api_view(['GET', 'POST'])
def apply_leave(request, id):
    Leave.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=60)
    ).delete()
    try:
        employee = Employee_Registration.objects.get(id=id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

    if request.method == 'GET':
        leaves = Leave.objects.filter(name=employee).order_by('-id')
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    print(request.data)
    if request.method == 'POST':
        serializer = LeaveSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(name=employee)
            return Response({"message": "Leave applied successfully"})

        return Response(serializer.errors, status=400)
    print(serializer.errors)

@api_view(['PATCH'])
def update_leave_status(request, id):

    try:
        leave = Leave.objects.get(id=id)
    except Leave.DoesNotExist:
        return Response({"error": "Leave not found"}, status=404)

    # Only update status field
    status_value = request.data.get("status")

    if status_value not in ["approved", "rejected"]:
        return Response({"error": "Invalid status"}, status=400)

    leave.status = status_value
    leave.save()

    return Response({
        "message": f"Leave {status_value} successfully",
        "id": leave.id,
        "status": leave.status
    })


@csrf_exempt
@api_view(['GET'])
def leave_details(request,id):
    try:
        employee = Employee_Registration.objects.get(id=id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)
    # if request.method == 'GET':
    casual_taken = Leave.objects.filter(
    name=employee,
    leave_type="casual").count()
    sick_taken = Leave.objects.filter(
    name=employee,
    leave_type="medical").count()
    lop_taken = Leave.objects.filter(name=employee,leave_type = 'nopay').count()
    taken = casual_taken + sick_taken + lop_taken
    remaining = 24-taken
    casual_remaining =12-casual_taken
    sick_remaining = 12-sick_taken
    data = {
        "casual_taken": casual_taken,
        "casual_remaining":casual_remaining,
        "sick_remaining":sick_remaining,
        "sick_taken": sick_taken,
        "remaining":remaining,
        "taken":taken,
        "lop":lop_taken
    }
    print(data)
    serializer = LeaveSummarySerializer(data)
    return Response(serializer.data)




# @api_view(['PATCH'])
# def update_employee_details(request, id):
#     try:
#        other_details = Employee_other_details.objects.get(name_id=id)
#     except Employee_Registration.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=404)

#     serializer = Employee_other_details_serializer(other_details, data=request.data, partial=True)

#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Profile updated successfully", "data": serializer.data})


@api_view(['PATCH'])
def update_employee_details(request, id):

    other_details, created = Employee_other_details.objects.get_or_create(name_id=id)

    serializer = Employee_other_details_serializer(
        other_details,
      
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully",
            "data": serializer.data
        })

    return Response(serializer.errors, status=400)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_documents(request, id):
    employee = Employee_Registration.objects.get(id=id)
    serializer = Employee_documents_serializer(data = request.data)
    if serializer.is_valid():
        serializer.save(employee = employee)
        return Response({
            "message": "Document uploaded successfully",
            "data": serializer.data
        })
    print(serializer.errors)
    return Response(serializer.errors, status=400)
    # if 'profile' in data:
    #     profile_data = data['profile']
    #     profile_obj, created = Employee_other_details.objects.get_or_create(name=employee)
    #     serializer = Employee_other_details_serializer(profile_obj, data=profile_data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response_data['profile'] = serializer.data
    #     else:
    #         return Response({"profile_errors": serializer.errors}, status=400)
    # if 'bank' in data:
    #     bank_data = data['bank']
    #     bank_obj, created = Employee_Bank_details.objects.get_or_create(name=employee)
    #     serializer = Employee_bank_details_serializer(bank_obj, data=bank_data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response_data['bank'] = serializer.data
    #     else:
    #         return Response({"bank_errors": serializer.errors}, status=400)

    # if not response_data:
    #     return Response({"error": "No valid data provided"}, status=400)
    # return Response(response_data, status=200)    


@api_view(['GET'])
def get_employee_payslips(request,id):
    employee = Employee_Registration.objects.get(id=id)
    payslips = Payslip.objects.filter(name=employee)
    serializer = PayslipSerializer(payslips, many=True)
    return Response(serializer.data)  


@api_view(['GET'])
def get_employee_documents(request,id):
    employee = Employee_Registration.objects.get(id=id)
    documents = Employee_main_files.objects.filter(employee=employee)
    serializer = Employee_main_files_Serializer(documents,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def attendance_status(request, id):

    today = timezone.localdate()

    attendance = Employee_attendence_details.objects.filter(
        name_id=id,
        date=today
    ).first()

    if not attendance:
        return Response({"status": "not_punched"})

    if attendance.checkin and not attendance.checkout:
        return Response({
            "status": "punched_in",
            "checkin": attendance.checkin
        })

    if attendance.checkout:
        return Response({
            "status": "punched_out"
        })