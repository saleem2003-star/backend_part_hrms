from django.db import models

# Create your models here.
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