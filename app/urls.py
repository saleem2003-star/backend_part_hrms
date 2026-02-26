from django.urls import path
from .views import employee_data,create_data

urlpatterns = [
    path("employees/", employee_data),
    path("create/",create_data)
    
]