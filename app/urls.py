from django.urls import path
from .views import employee_data,create_data,employee_login,employee_dashboard,employee_attendence,employee_attendence_create,attendence_logout

urlpatterns = [
    path("employees/", employee_data),
    path("create/",create_data),
    path("employee/login/",employee_login),
    path("employee/dashboard/<int:id>/",employee_dashboard),
    path('employee/attendence/',employee_attendence),
    path('employee-attendence/create/',employee_attendence_create),
    path('employee-attendece/checkout/',attendence_logout)
   
]