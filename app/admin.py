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

admin.site.register(AssetRequest)

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id','emp_id','employee','email','asset_type','model_details','assigned_date','status')
admin.site.register(Asset, AssetAdmin)
admin.site.register(ReturnAsset)

class AttendanceRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'clock_in', 'clock_out', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('employee__name',)

admin.site.register(AttendanceRequest, AttendanceRequestAdmin)


@admin.register(Employee_Break_details)
class EmployeeBreakDetailsAdmin(admin.ModelAdmin):
    # This controls which columns show up in the admin list view
    list_display = ('employee', 'date', 'break_type', 'start_time', 'end_time', 'duration')
    
    # Adds a filter sidebar to filter by date, type, or employee
    list_filter = ('date', 'break_type')
    
    # Adds a search bar to search by employee name
    search_fields = ('employee__name', 'break_type')