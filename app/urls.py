from django.urls import path
from .views import *

urlpatterns = [
    path("employees/", employee_data),
    path("create/",create_data),
    path("employee/login/",employee_login),
    path("employee/dashboard/<int:id>/",employee_dashboard),
    path('employee/attendence/',employee_attendence),
    path('employee-attendence/create/',employee_attendence_create),
    path('employee-attendence/checkout/',attendence_logout),
    path('employee/apply-leave/<int:id>/',apply_leave),
    path('employee/update/<int:id>/',update_leave_status),
    path('employee/leaves/<int:id>/',leave_details),
    path('employee-payslips/<int:id>/',get_employee_payslips),
    path('update-employee/<int:id>/',update_employee_details),
    path('upload-documents/<int:id>/',upload_documents),
    path('employee-details/<int:id>/',admin_employee),
    path('attendence-status/<int:id>/',attendance_status),
    path('employee-documents/<int:id>/',get_employee_documents),
    path('birthdays/',birthdays),
    path('leave-approvals/',leave_approvals),
    path('employee-attendence-history/<int:id>/',employee_attendence_history)
    
]



