from django.shortcuts import render
from django.shortcuts import render
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import generics, response
from .querysets import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class EmployeeCreate(generics.CreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes=[IsHR | IsDepartmentManager]
    
    def post(self,request, *args, **kwargs):
        _mutable=request.data._mutable
        request.data._mutable=True
        request.data['create_id']=request.user.id
        request.data._mutable=_mutable
        
        return EmployeeCreate.create(self, request, *args, **kwargs)
  
class EmployeeList(generics.ListAPIView, EmployeeQueryset):
    
    def get_queryset(self):
       
       user=self.request.user.users.all().values_list('role__role_name')
       
       if ('HR',) in list(user):
           return self.queryset
       
       if ('DM',) in list(user):
           a=super().employee_queryset_department_manager()
           return a 
       
       if ('DE',) in list(user):
           a=super().employee_queryset_department_employee()
           return a 
    
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    filter_backends=[DjangoFilterBackend]
    filter_fields=['emp_no','first_name','last_name','gen','user_position']
    permission_classes=[IsHR | IsDepartmentManager | IsEmployee] 


class EmployeeDetail(generics.RetrieveAPIView, EmployeeQueryset):
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')
        
        if ('HR',) in list(user):
            return self.queryset
       
        if ('DM',) in list(user):
           a=super().employee_queryset_department_manager()
           return a 
        
        if ('DE',) in list(user):
           a=super().employee_queryset_department_employee()
           return a 
    
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes=[IsHR | IsDepartmentManager| IsEmployee]
    
    
class EmployeeUpdate(generics.RetrieveUpdateAPIView, EmployeeQueryset):
    
    def get_queryset(self):
        
        user=self.request.user.users.all().values_list('role__role_name')
        if ('HR',) in list(user):
           return self.queryset
       
        if ('DM',) in list(user):
           a=super().employee_queryset_department_manager()
           return a 
        
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes=[IsHR | IsDepartmentManager]
        
        
class EmployeeDelete(generics.DestroyAPIView):
    
    queryset=Employee.objects.all()
    serializers_class=EmployeeSerializer
    permission_classes=[IsHR]
        
    def delete(self, request, *args, **kwargs):
        employee=Employee.objects.get(id=kwargs.get('pk'))
        if not employee.active:
            return Response({'error_message':'Could not delete!'},status=status_HTTP_405_METHOD_NOT_ALLOWED)
            return super(EmployeeDelete,self).delete(request=request, *args, **kwargs)
