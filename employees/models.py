from django.db import models
from permission_management.models import *
from departments.models import *
from users.models import *

# Create your models here.
class Employee(models.Model):
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    emp_no = models.IntegerField(primary_key=True)
    user = models.OneToOneField('users.Users', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='employee')
    phone_no = models.CharField(max_length = 10,default='')
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gen= models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_position=models.ForeignKey('users.UserRole', on_delete=models.DO_NOTHING,null=True, blank=True, related_name='employee')
    department=models.ForeignKey('departments.Department', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='employee')
    leave_time=models.IntegerField(default=160)
    manager=models.BooleanField(default=False)
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        db_table = 'employee'
