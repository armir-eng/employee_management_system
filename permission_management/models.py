from django.db import models
from django.db.models import IntegerField
from django.conf import settings
from django.utils import timezone
from datetime import date,timedelta
from django_pandas.managers import DataFrameManager
from departments.models import *
from employees.models import *
from datetime import datetime
# Create your models here.


class Leave (models.Model):
    
    STATUS = (('approved','APPROVED'),('unapproved','UNAPPROVED'),('decline','DECLINED'))
    employee = models.ForeignKey('employees.Employee', on_delete=models.DO_NOTHING, related_name='leave', null=True)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    status = models.CharField(choices=STATUS,  default='Not Approved',max_length=15)
    active = models.BooleanField(default=True)
    reason = models.CharField(max_length=50,default='')    
    approval_date=models.DateTimeField( null=True, blank=True)
    objects = DataFrameManager() 

    def __str__(self):
        return '%s : %s | %s' %(self.employee, self.start, self.end)     

    
class Holiday(models.Model):
    
    name=models.CharField(max_length=40)
    date=models.DateField(blank=False)    
    leave = models.ManyToManyField('Leave', blank=True) #Duke zgjedhur edhe ketu tipin ManytoMany, aplikohet mundesia qe nje dite pushimi te perfishet brenda intervalit te disa lejeve, si dhe nje leje mund te perfshije ne intervalin e vet disa dite pushimi.
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    



