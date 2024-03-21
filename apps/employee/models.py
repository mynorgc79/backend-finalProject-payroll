from django.db import models

# Employee 

class Employee(models.Model):

    """Employee Model"""
   
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    picture = models.CharField(max_length=200)
    dpi = models.CharField(max_length=20)
    date_hiring = models.DateField(blank=True, null=True)
    date_completion = models.DateField(blank=True, null=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=10)
    base_salary = models.IntegerField()
    base_salary_initial = models.IntegerField()
    head_department = models.BooleanField(default=False)
    method_payment = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    department = models.IntegerField(default=1) #ForeignKey
    job_position = models.IntegerField(default=1) #ForeignKey
    user = models.IntegerField(default=3) #ForeignKey 
    company = models.IntegerField(default=1) #ForeignKey
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class SalaryIncrease(models.Model):

    """Salary Increase Model"""

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) #ForeignKey
    amount = models.IntegerField()
    reason = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reason}"
    
    def apply_increase(self):
        super().save()
        self.employee.base_salary += self.amount
        self.employee.save()


class Department(models.Model):

    """Department Model"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    company = models.IntegerField() #ForeignKey
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"