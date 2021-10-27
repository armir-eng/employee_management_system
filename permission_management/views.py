from permission_management.models import * 
from permission_management.serializers import *
from departments.models import *
from employees.models import *
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, response
from rest_framework import status
from rest_framework.response import Response
from permission_management.permissions import *
from rest_pandas.renderers import PandasExcelRenderer, PandasCSVRenderer
from .querysets import *
from datetime import datetime
from django.db.models import F


class LeaveCreate(generics.CreateAPIView):
    
    queryset = Leave.objects.all()
    serializer_class = LeaveCreateSerializer
    permission_classes=[IsEmployee | IsDepartmentManager] 
    
    def post(self,request, *args, **kwargs):
        return LeaveCreate.create(self, request, *args, **kwargs)
    

class LeaveList(generics.ListAPIView, LeaveQueryset):
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset.all()
       
        if ('DM',) in list(user):
            a=super().leave_queryset_department_manager()
            return a

        if('DE',) in list(user):
            a=super().leave_queryset_department_employee()
            return a
    
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes=[IsDepartmentManager | IsHR | IsEmployee]
    
    

class LeaveDetail(generics.RetrieveAPIView, LeaveQueryset):
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')
        print(user)
       
        if ('HR',) in list(user):
            return self.queryset
       
        if ('DM',) in list(user):
           a=super().leave_queryset_department_manager()
           return a
       
        if ('DE',) in list(user):
           a=super().leave_queryset_department_employee()
           return a
    
    queryset=Leave.objects.all()   
    serializer_class = LeaveSerializer
    permission_classe=[IsHR | IsDepartmentManager| IsEmployee]


class Leave_Approval(generics.RetrieveUpdateAPIView, LeaveQueryset):
    
    def get_queryset(self):
        
        user=self.request.user.users.all().values_list('role__role_name')
        if ('HR',) in list(user):
           return self.queryset
       
        if ('DM',) in list(user):
           a=super().leave_queryset_department_manager_approval()
           return a 

    queryset = Leave.objects.all()
    serializer_class = Leave_2_Serializer
    permission_classes=[IsDepartmentManager | IsHR] 
    
    def put(self, request, *args, **kwargs):
        
        leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk'])
        
        if leave.status=='approved': #In case the superior wrongly makes an approval, he can recover it the next time, by not further reducing the remaining leave hours with the reapproval of that leave.
            super().leave_update_holiday_conditions()  #By these two rows, the compensation of hours spent from previous approval. 
            super().leave_data_update()       
            
            super().leave_approval_holiday_conditions() #Now, by the below rows, the final update of remaining time of leave time.
            super().leave_data_approval()       
            return Response(data=request.data, status=status.HTTP_200_OK)
            return leave_approval_holiday_conditions.employee
            return leave_data_approval.leave

        
        elif leave.status=='unapproved': #In case the approval is done for the first time, the necessary update is done on remaining hours of leave for the employee.
            
            if self.request.data['status'] == 'approved':
                super().leave_approval_holiday_conditions()
                super().leave_data_approval()       
                return Response(data=request.data, status=status.HTTP_200_OK)
                return leave_approval_holiday_conditions.employee
                return leave_data_approval.leave

        elif leave.status=='decline': #In case it is declined, there is no need for compensating action, like at the first condition.
            return Response("This leave has been declined by the applicant!", status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return self.update(request, *args, **kwargs) 


class LeaveUpdate(generics.RetrieveUpdateAPIView, LeaveQueryset): #This view is dedicated to logged-in user cancelling his own leave request, which he can do only within 48 hours after his superior has approved it.
    
    def get_queryset(self):
        
        user=self.request.user.users.all().values_list('role__role_name')
    
        if ('DM',) in list(user):
            a=super().leave_queryset_department_manager()
            return a
        
        if ('DE',) in list(user):
           a=super().leave_queryset_department_employee()
           return a
        
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes=[IsDepartmentManager | IsEmployee ]
    
    def put(self, request, *args, **kwargs):
        
        leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk']) #This gets the leave that is going to be declined.
        
        if leave.status=='decline': #This condition is necessary because if the cancelling is done multiple times, then the compensated hours are added any time it is done. This way, the remaining leave time is infinitely added, so anyone would abuse with this fault of the system.
            return Response("This leave has been declined once!", status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        
        elif leave.status=='approved': 
            
            if self.request.data['status']=='approved' or self.request.data['status']=='unapproved': #If one of these options in the select list is chosen, the below message is shown.
                return Response("Only your superior can approve or not the leave!" ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
            elif self.request.data['status']=='decline': #If the 'DECLINE' option is selected
                a=str(datetime.now()) #This saves the time when leave is finaly declined.
                b=str(leave.approval_date) #This saves the time when leave is finaly approved.(that is found at initial leave data)
                #This does the necessary conversion of two above dates into datetime ojects. This is important so that the difference between two moments can be calculated. 
                d1=datetime.strptime(a,"%Y-%m-%d %H:%M:%S.%f")
                d2=datetime.strptime(b,"%Y-%m-%d %H:%M:%S.%f")
                dif=d1-d2
                difference=dif.seconds #I chose the difference to be calculated in seconds, for a higher accuracy.
                
                if difference<=172800: #This block means: "If two days have not passed from the approval moment, then the employee can cancel the leave and the hours spent are compensated".
                   super().leave_update_holiday_conditions()
                   super().leave_data_update()       
                   return Response(data=request.data, status=status.HTTP_200_OK)
                   return leave_update_holiday_conditions.employee
                   return leave_data_update.leave
                
                    
                else:
                    return Response("You cannot decline the leave more than 2 days after it has been approved!", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return self.update(request, *args, **kwargs)



from rest_pandas import PandasView
import pandas

class LeaveView(PandasView, LeaveQueryset): #All this view does the leave report generation.
    
    permission_classes=[IsHR | IsDepartmentManager]
    
    def get_queryset(self):
        user=self.request.user.users.all().values_list('role__role_name')
        
        if ('HR',) in list(user):
            return self.queryset.all()
       
        if ('DM',) in list(user):
            a=super().leave_queryset_department_manager()
            return a
    
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer  # extends ModelSerializer
    renderer_classes = [PandasExcelRenderer]
    
    def get_pandas_filename(self, request, format):
       
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Leave Report"  # Extension will be appended automatically
        
        else:
            # Default filename from URL (no Content-Disposition header)
            return None


class LeaveDelete(generics.DestroyAPIView, LeaveQueryset):
    
    def get_queryset(self):
        
        user=self.request.user.users.all().values_list('role__role_name')
        
        if ('HR',) in list(user):
            return self.queryset
       
        if ('DM',) in list(user):
            a=super().leave_queryset_department_manager()
            return a
    
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsHR | IsDepartmentManager]
    
    def delete(self, request, LeaveDelete=None, *args, **kwargs):
        leave = Leave.objects.get(id=kwargs.get('pk'))
        if not leave.active:
            return Response( "Could not delete for some reason!",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request=request, *args, **kwargs)  
    
class HolidayCreate(generics.CreateAPIView):
    
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes=[IsHR]
        
    def post(self, *args, **kwargs):
        return HolidayCreate.create(self, *args, **kwargs)

class HolidayList(generics.ListCreateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
         
class HolidayDetail(generics.RetrieveAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

class HolidayUpdate(generics.UpdateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes=[IsHR]

class HolidayDelete(generics.DestroyAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes=[IsHR] 

    def delete(self, request, HolidaysDelete=None, *args, **kwargs):
        holidays = Holiday.objects.get(id=kwargs.get('pk'))
        if not holidays.active:
            return Response({'error_message': "Could not delete"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(HolidayDelete, self).delete(request=request, *args, **kwargs)
