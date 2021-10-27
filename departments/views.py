from django.shortcuts import render
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import generics, response
from .querysets import *
from django_filters.rest_framework import DjangoFilterBackend
from permission_management.models import *
from employees.models import *

# Create your views here.

class DepartmentCreate(generics.CreateAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes=[IsHR]
    
    def post(self, *args, **kwargs):
        return DepartmentCreate.create(self, *args, **kwargs)

class DepartmentList(generics.ListAPIView, DepartmentQueryset):
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')
        
        if ('HR',) in list(user):
            return self.queryset
       
        if ('DM',) in list(user):
            a=super().department_queryset_department_manager()
            return a
    
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer
    filter_backends=[DjangoFilterBackend]
    filter_fields=['dept_no','dept_name','dept_manager','active'] 
    permission_classes=[IsHR | IsDepartmentManager]
     

class DepartmentDetail(generics.RetrieveAPIView, DepartmentQueryset):
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')
        x=list(user)
        print(x)
        
        if ('HR',) in list(user):
            return self.queryset
       
        if ('DM',) in list(user):
            a=super().department_queryset_department_manager()
            return a
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes=[IsHR | IsDepartmentManager]

class DepartmentUpdate(generics.UpdateAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes=[IsHR]

class DepartmentDelete(generics.DestroyAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes=[IsHR] 
    
    def delete(self, request, *args, **kwargs):
        department = Department.objects.get(id=kwargs.get('pk'))
        if not department.active:
            return Response({'error_message':"Could not delete"},
            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(DepartmentDelete, self).delete(request = request, *args, **kwargs)
