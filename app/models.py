from django.db import models

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
  
class Employee_attendence(models.Model):
    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    checkin= models.DateTimeField()
    checkout = models.DateTimeField( null=True , blank=True)


class Employee_payslip(models.Model):
    name =models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    this_month_pay = models.BigIntegerField()
    pf_deduction = models.FloatField()
    total_working_Days = models.CharField(max_length=100)
    
class Employee_documents(models.Model):
    name = models.ForeignKey(Employee_Registration,on_delete=models.CASCADE)
    Aadhar = models.FileField()
    pan = models.FileField()
    ssc = models.FileField()
    inter = models.FileField()
    graduation = models.FileField()
    photo = models.FileField()    
# class Attendence_today(models.Model): 
#     user = models.OneToOneField(Employee_Registration,on_delete=models.CASCADE)
    