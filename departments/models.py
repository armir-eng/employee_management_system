from django.db import models
from permission_management.models import *
from employees.models import *
# Create your models here.

class Department(models.Model):
    
    dept_no = models.CharField(primary_key=True, max_length=4)
    dept_name = models.CharField(unique=True, max_length=40)
    dept_manager = models.OneToOneField('employees.Employee',on_delete=models.DO_NOTHING, null=True, blank=True, related_name='dept_manager') 
    parent = models.ManyToManyField('self', blank=True, symmetrical=False )  #I chose this field to be ManyToMany type beecause this way, a "parent" department can have many inferior ones and any department can have many superior departments. This makes the hierarchy structure very accurate and flexible.
    dept_parent=models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'departments'
    
    def __str__(self):
        return '%s' % (self.dept_name)