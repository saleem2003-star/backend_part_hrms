from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Employee_Registration)
admin.site.register(Employee_attendence_details)
admin.site.register(Employee_other_details)
admin.site.register(Employee_Bank_details)
admin.site.register(Employee_statuory_information)
admin.site.register(Leave)
admin.site.register(Payslip)
admin.site.register(Employee_main_files)
