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
    path('employee-attendence-history/<int:id>/',employee_attendence_history),
    path('asset-request/', create_asset_request),
    path('asset-return/',Create_Return_Asset),
    path("return-assets/", get_return_assets),
    path("return-status/<int:pk>/", update_return_status),
    path("return-assets/<int:pk>/", delete_return_asset),
    path('assets/<int:pk>/', asset_update_delete),
    path('assets/', get_assets),
    path('assets/save/', save_asset),
    path('employee-assets/<str:emp_id>/', get_employee_assets),
    path('admin/asset-requests/', get_all_asset_requests),
    path('admin/asset-request-status/<int:pk>/', update_asset_request_status),
    
    path('attendance-request/create/', create_attendance_request), # For Employee Page
    path('admin/attendance-requests/', get_attendance_requests),   # For Admin Table
    path('admin/attendance-status/<int:pk>/', update_attendance_request_status), # For Admin Action

    path('employee-break/start/', start_break),
    path('employee-break/end/', end_break),
    
    path('today-attendance/', todays_attendance),
    path('attendance-graph/', attendance_graph),
    path('attendance/monthly-summary/', monthly_attendance_summary),
]



