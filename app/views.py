from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee_Registration,Employee_attendence
from .serializers import Employee_serializer,EmployeeLoginSerializer,Employee_attendence_serializer,EmployeeCheckInSerializer
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

# @csrf_exempt
# @api_view(['GET','POST'])      
# def employe_dashboard(request):
#     if request.method == 'GET' :
           
# @csrf_exempt
# @api_view(['GET','POST'])
# def attendence(request):
#     if request.method == 'GET':
#         employee = Employee_Registration.objects.filter(id=1)
    
        
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
        employees = Employee_attendence.objects.all()
        serializer = Employee_attendence_serializer(employees, many=True)
        return Response(serializer.data)
    print(employees) 
    
# @csrf_exempt
# @api_view(['GET','POST'])
# def employee_attendence_create(request):
#     if request.method == 'POST':
#         serializer = Employee_attendence_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print("Saved data:", serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors)
        
from django.utils import timezone



@csrf_exempt
@api_view(['GET','POST'])
def employee_attendence_create(request):
    employee_id = request.data.get('id')
    print(employee_id)
    if not employee_id:
        return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        employee = Employee_Registration.objects.get(id=employee_id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    attendance = Employee_attendence.objects.create(
        name=employee,
        checkin=timezone.now()
    )

    serializer = Employee_attendence_serializer(attendance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['PUT'])
def attendence_logout(request):
    if request.method == 'PUT':
        employee_id = request.data.get('id')
        employee = Employee_Registration.objects.get(id=employee_id)
        attendence = Employee_attendence.objects.filter(name = employee,checkout__isnull = True)
        attendence.checkout = timezone.now()
        attendence.save(update_fields=['checkout'])

# print(Employee_attendence.objects.all())     
# @csrf_exempt
# @api_view(['GET','POST'])
# def attendence(request):
#     if request.method == 'POST':
        

# @csrf_exempt
# @api_view(['POST'])
# def employee_login(request):
#     serializer = EmployeeLoginSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response({
#             "status": "error",
#             "message": "Invalid email or password"
#         }, status=400)

#     employee = serializer.validated_data['employee']
#     emp_serializer = Employee_serializer(employee)

#     return Response({
#         "status": "success",
#         "message": "Login successful",
#         "employee_data": emp_serializer.data
#     })
    
     
@csrf_exempt
@api_view(['GET','POST'])
def employee_dashboard(request,id):
    
    employee = Employee_Registration.objects.get(id=id)
    serializer = Employee_serializer(employee)
    return Response(serializer.data)
