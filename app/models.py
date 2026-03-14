from django.db import models
from django.utils import timezone

class Employee_Registration(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.CharField(max_length=200)
    salary = models.BigIntegerField()
    department = models.CharField(max_length=200)
    joining = models.DateField()
    full_time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    manager_employee = models.CharField(max_length = 200)
    password = models.CharField(max_length=40)
    employee_id = models.IntegerField()
    
    def __str__(self):
        return self.name


# class Employee_Documents(models.Model):
#     name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
#     doc_type = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     file = models.FileField(upload_to='documents/',null=True, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.name} - {self.description}"


class Employee_main_files(models.Model):
    employee = models.ForeignKey(Employee_Registration, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.doc_type}"
    
class Employee_other_details(models.Model):
    name =models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    mobile = models.BigIntegerField(null=True,blank=True)
    marital_status =models.CharField(max_length=100,null=True,blank=True)
    Gender =  models.CharField(max_length=20,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f"{self.name} - {self.mobile}"



class Employee_Bank_details(models.Model):
    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    acc_no =  models.BigIntegerField(null=True,blank=True)
    ifsc_code = models.CharField(max_length=15,null=True,blank=True)
    holder_name = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.BigIntegerField(null=True,blank=True)
    branch = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f"{self.name} - {self.bank_name}"



class Employee_statuory_information(models.Model):
    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    pan = models.CharField(max_length=10)
    pf_uan = models.CharField(max_length=30)
    profesional_tax = models.CharField(max_length=100)
    lwf_status = models.CharField(max_length=100)
    esic_status=models.CharField(max_length=100)
    esic_ip_number= models.BigIntegerField()
    def __str__(self):
        return f"{self.name} - {self.pan}"



class Employee_attendence_details(models.Model):
    name = models.ForeignKey(Employee_Registration, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)  # Make sure this line exists
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.checkin and self.checkout:
            self.duration = self.checkout - self.checkin
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'date')
    
    def __str__(self):
        return f"{self.name} - {self.checkin}"
    
    
class Employee_payslip(models.Model):
    name =models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    this_month_pay = models.BigIntegerField()
    pf_deduction = models.FloatField()
    total_working_Days = models.CharField(max_length=100)
    def __str__(self):
        return self.name

  
 

class Payslip(models.Model):
    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    # employee_id=models.CharField(max_length=20)
    # employee_name=models.CharField(max_length=100)
    month=models.CharField(max_length=20)
    basic_salary=models.FloatField()
    gross_salary=models.FloatField()
    pf_amount=models.FloatField()
    professional_tax = models.FloatField()
    lop_days = models.IntegerField()
    lop_amount = models.FloatField()
    net_salary = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.month}"

class Leave(models.Model):

    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    number_of_days = models.IntegerField()
    remaining_leaves = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.leave_type}"

class Asset(models.Model):

    
    asset_id = models.CharField(max_length=100, null=True, blank=True)
    emp_id = models.CharField(max_length=50)
    employee = models.CharField(max_length=100)
    email = models.EmailField()
    asset_type = models.CharField(max_length=50)
    model_details = models.CharField(max_length=200)
    assigned_date = models.DateField()
    status = models.CharField(max_length=50, default='assigned')

    def __str__(self):
        return f"{self.asset_id} - {self.employee}"
    
class AssetRequest(models.Model):
    emp_id = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=100)
    asset_category = models.CharField(max_length=100)
    model_detail = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - {self.asset_category}"
    
class ReturnAsset(models.Model):
    emp_id = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    condition=models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return f"{self.employee_name}-{self.asset_type}"

class AttendanceRequest(models.Model):
    employee = models.ForeignKey(Employee_Registration, on_delete=models.CASCADE)
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=50, default='Pending') # Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date} Request"
    

class Employee_Break_details(models.Model):
    employee = models.ForeignKey(Employee_Registration, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    break_type = models.CharField(max_length=50) # Will store 'lunch' or 'normal'
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate break duration when ending the break
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.break_type} on {self.date}"