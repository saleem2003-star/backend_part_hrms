from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
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



@api_view(['GET'])
def employee_attendence_history(request, id):
    attendances = Employee_attendence_details.objects.filter(name_id=id).order_by('-date')
    serializer = Employee_attendence_serializer(attendances, many=True)
    return Response(serializer.data)
# @csrf_exempt
# @api_view(['GET','POST'])
# def employee_attendence_history(requset,id):
#     employee = Employee_Registration.objects.get(id=id)
#     serializer = Employee_attendence_serializer(name=employee)
#     return Response(serializer.data)
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
        


from datetime import date
def birthdays(request):
    today = date.today()
    employees = Employee_Registration.objects.all()

    today_birthdays = []
    upcoming_birthdays = []

    for emp in employees:
        try:
            details = Employee_other_details.objects.get(name=emp)
            emp_dob = details.dob
        except Employee_other_details.DoesNotExist:
            continue 

        if emp_dob.month == today.month and emp_dob.day == today.day:
            today_birthdays.append({
                "name": emp.name,
                "dob": str(emp_dob),
                
            })
        else:
            upcoming_birthdays.append({
                "name": emp.name,
                "dob": str(emp_dob),
               
            })
    upcoming_birthdays.sort(key=lambda x: x["dob"])

    return JsonResponse({
        "today": today_birthdays,
        "upcoming": upcoming_birthdays
    })
    


def leave_approvals(request):
    approvals = []
    pending_leaves = Leave.objects.filter(status='pending')
    for leave in pending_leaves:
        approvals.append({
            'id':leave.id,
            'name': leave.name.name,
            'details': leave.leave_type,
            'duration': f"from {leave.from_date} to {leave.to_date}",
            'reason':leave.reason,
            'days': leave.number_of_days
        })
    return JsonResponse({
        'data': approvals
    })
    
@api_view(['POST'])
def create_asset_request(request):

    print("REQUEST DATA:", request.data)

    serializer = AssetRequestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Request saved"})

    print("ERRORS:", serializer.errors)

    return Response(serializer.errors, status=400)


@api_view(["POST"])
def Create_Return_Asset(request):
    serializer=ReturnAssetSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Request saved"})
    print("Errors:",serializer.errors)
    
    return Response(serializer.errors, status=400)
@api_view(["GET"])
def get_return_assets(request):
    assets = ReturnAsset.objects.all().order_by("-id")
    serializer = ReturnAssetSerializers(assets, many=True)
    return Response(serializer.data)

@api_view(["PATCH"])
def update_return_status(request, pk):

    try:
        asset = ReturnAsset.objects.get(id=pk)

        status = request.data.get("status")
        asset.status = status
        asset.save()

        if status == "received":
            Asset.objects.filter(
                emp_id=asset.emp_id,
                asset_type=asset.asset_type
            ).update(status="returned")

        return Response({"message": "Status updated successfully"})

    except ReturnAsset.DoesNotExist:
        return Response({"error": "Return request not found"}, status=404)
    
@api_view(["DELETE"])
def delete_return_asset(request, pk):

    try:
        asset = ReturnAsset.objects.get(id=pk)
        asset.delete()
        return Response({"message":"Deleted"})
    except ReturnAsset.DoesNotExist:
        return Response({"error":"Not found"}, status=404)
    
@api_view(["PATCH", "DELETE"])
def asset_update_delete(request, pk):  # Change asset_id to pk
    try:
        # Change lookup to use the automatic database ID
        asset = Asset.objects.get(id=pk) 
    except Asset.DoesNotExist:
        return Response({"error": "Asset not found"}, status=404)

    if request.method == "PATCH":
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400) # Return errors if invalid

    if request.method == "DELETE":
        asset.delete()
        return Response({"message": "Deleted successfully"})
    
    
@api_view(['GET'])
def get_assets(request):
    assets = Asset.objects.all()
    serializer = AssetSerializer(assets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def save_asset(request):
    serializer = AssetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['GET'])
def get_employee_assets(request, emp_id):
    assets = Asset.objects.filter(emp_id=emp_id)
    serializer = AssetSerializer(assets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_asset_requests(request):
    requests = AssetRequest.objects.filter(status='Pending').order_by('-id')
    serializer = AssetRequestSerializer(requests, many=True)
    return Response(serializer.data)

# 2. APPROVE/REJECT REQUEST (Fixed with Error Handling)
@api_view(['PATCH'])
def update_asset_request_status(request, pk):
    try:
        # Get the request object
        asset_request = AssetRequest.objects.get(id=pk)
        
        # Get status from frontend
        new_status = request.data.get('status') # 'Approved' or 'Rejected'
        
        print(f"Processing Request ID: {pk} | New Status: {new_status}") # Debug Print

        # Update the request status
        asset_request.status = new_status
        asset_request.save()

        # --- LOGIC: CREATE ASSET IF APPROVED ---
        if new_status == 'Approved':
            try:
                # Create the Asset
                new_asset = Asset.objects.create(
                    asset_id=f"AST-{asset_request.id}", # Temp ID
                    emp_id=asset_request.emp_id,
                    employee=asset_request.employee_name,
                    email="employee@example.com", # Placeholder (Required by Model)
                    asset_type=asset_request.asset_category,
                    model_details=asset_request.model_detail, 
                    assigned_date=timezone.now().date(), # FIXED DATE FORMAT
                    status="assigned"
                )
                print(f"Asset Created Successfully: {new_asset.asset_id}") # Debug Print
                return Response({"message": "Request Approved & Asset Created!"})
            
            except Exception as e:
                # If creating the asset fails, print the error
                print(f"CRITICAL ERROR CREATING ASSET: {str(e)}")
                return Response({"error": f"Failed to create asset: {str(e)}"}, status=500)

        return Response({"message": f"Request marked as {new_status}"})

    except AssetRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)
    
    except Exception as e:
        print(f"GENERAL ERROR: {str(e)}")
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
def create_attendance_request(request):
    try:
        # We expect data like: { "employee": 8, "date": "2024-03-12", "clock_in": "09:00", "clock_out": "18:00", "reason": "Forgot punch" }
        serializer = AttendanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Correction request submitted successfully!"}, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# 2. ADMIN GETS PENDING REQUESTS (GET)
@api_view(['GET'])
def get_attendance_requests(request):
    requests = AttendanceRequest.objects.filter(status='Pending').order_by('-created_at')
    serializer = AttendanceRequestSerializer(requests, many=True)
    return Response(serializer.data)

# 3. ADMIN APPROVES REQUEST (PATCH)
@api_view(['PATCH'])
def update_attendance_request_status(request, pk):
    try:
        req = AttendanceRequest.objects.get(id=pk)
        new_status = request.data.get('status')
        req.status = new_status
        req.save()

        # --- THE MAGIC LOGIC: UPDATE MAIN TABLE IF APPROVED ---
        if new_status == 'Approved':
            # 1. Find the main attendance record for that Employee + Date
            # get_or_create handles if the record didn't exist (e.g. they forgot to punch in at all)
            main_record, created = Employee_attendence_details.objects.get_or_create(
                name=req.employee,
                date=req.date
            )

            # 2. Combine the Date from request with the Time from request to make DateTime
            # Because your main table uses DateTimeField
            if req.clock_in:
                main_record.checkin = datetime.combine(req.date, req.clock_in)
            
            if req.clock_out:
                main_record.checkout = datetime.combine(req.date, req.clock_out)

            main_record.save()
            return Response({"message": "Approved and Attendance Updated!"})

        return Response({"message": "Request Rejected"})

    except AttendanceRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
def start_break(request):
    employee_id = request.data.get('id')
    break_type = request.data.get('break_type') # 'lunch' or 'normal'

    if not employee_id or not break_type:
        return Response({"error": "Employee ID and break type are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        employee = Employee_Registration.objects.get(id=employee_id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is already on a break that hasn't ended yet
    active_break = Employee_Break_details.objects.filter(
    employee=employee,
    end_time__isnull=True
).first()

    if active_break:
        return Response({"error": "Already on an active break"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the new break session
    break_record = Employee_Break_details.objects.create(
        employee=employee,
        date=timezone.localdate(),
        break_type=break_type,
        start_time=timezone.now()
    )
    
    serializer = EmployeeBreakSerializer(break_record)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['PUT'])
def end_break(request):
    employee_id = request.data.get('id')
    
    if not employee_id:
        return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        employee = Employee_Registration.objects.get(id=employee_id)
    except Employee_Registration.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    # Find the active break for today that hasn't been closed yet
    active_break = Employee_Break_details.objects.filter(
        employee=employee, 
        date=timezone.localdate(), 
        end_time__isnull=True
    ).order_by('-start_time').first()

    if not active_break:
        return Response({"error": "No active break found to end"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the end time and save (which triggers the duration calculation in the model)
    active_break.end_time = timezone.now()
    active_break.save()
    
    serializer = EmployeeBreakSerializer(active_break)
    return Response(serializer.data, status=status.HTTP_200_OK)