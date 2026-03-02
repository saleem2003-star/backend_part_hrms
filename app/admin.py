from django.contrib import admin

# Register your models here.
from .models import Employee_Registration,Employee_attendence
admin.site.register(Employee_Registration)
admin.site.register(Employee_attendence)