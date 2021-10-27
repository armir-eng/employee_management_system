from permission_management.models import *
from departments.models import * 
from employees.models import *
from datetime import datetime

class LeaveQueryset:
   
    def leave_queryset_department_manager_approval(self):
            emp=self.request.user.employee  #The employee corresponding to the logged-in user is got from the database.
            manager_employee=Department.objects.filter(dept_manager=emp.emp_no)
            parent_employee=Department.objects.filter(parent=emp.dept_manager.dept_no)
            all_depts=manager_employee | parent_employee
            all_emp=Employee.objects.filter(department__dept_no__in=all_depts, manager=False) #The second argument means that the manager can't approve his own leave request.
            leave=Leave.objects.filter(employee__emp_no__in=all_emp) 
            return leave

    def leave_queryset_department_manager(self):
            emp=self.request.user.employee   #The employee corresponding to the logged-in user is got from the database. 
            manager_employee=Department.objects.filter(dept_manager=emp.emp_no)   #This gets the department, whose manager is the logged-in user. 
            parent_employee=Department.objects.filter(parent=emp.dept_manager.dept_no)   #This gets the inferior departments of the above department.
            all_depts=manager_employee | parent_employee #Merges two querysets above.
            all_emp=Employee.objects.filter(department__dept_no__in=all_depts)  #This gets all employess of the filtered group of departments.
            leave=Leave.objects.filter(employee__emp_no__in=all_emp) #This gets the leaves of all employees got in the above row.
            return leave        
        
     
    def leave_queryset_department_employee(self):
            emp=self.request.user.employee
            leave=Leave.objects.filter(employee=emp)
            return leave                                                            

    
    def leave_data_approval(self): #Dedicated to updated the details of leave being approved or not. Whereas we need to apply lines of this function in the approval view conditions, I would be forced to repeat myself. Thus, to avoid this thing, the best solution would be putting these into a single function and then simply calling that when needed.
            
            leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk']) #This gets only the leave on which is acted (is approved or not, with the id defined at the view url).
            
            #This block makes necessary updates on the leave dealed with.
            leave.status=self.request.data['status']
            leave.start=self.request.data['start']
            leave.end=self.request.data['end']
            leave.reason=self.request.data['reason']
            leave.approval_date=datetime.now()
            if self.request.data['active'] == "true":
                leave.active=True 
            elif self.request.data['active'] == "false":
                leave.active=False 
            leave.save()
    
    
    def leave_data_update(self): #Dedicated to updating of details of the leave that is being updated. The difference here is that is not including the command theat updates the approval date. The reason is the same as one expressed at the above definition.
            
            leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk']) #This gets only the specific leave of logged-in employee, which he wants to cancel(the one with the id defined at url of view)
            
            #This block does the same thing as the above function (data update after leave decline)
            leave.status=self.request.data['status']
            leave.start=self.request.data['start']
            leave.end=self.request.data['end']
            leave.reason=self.request.data['reason']
            if self.request.data['active'] == "true":
                leave.active=True 
            elif self.request.data['active'] == "false":
                leave.active=False 
            leave.save()
    
    
    def leave_approval_holiday_conditions(self): #This function assigns the remaining leave time for the applicant, after his/her superior has approved it.
        
        leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk'])
        holiday=Holiday.objects.filter(leave=leave)
        employee=Employee.objects.get(emp_no=self.request.data['employee'])
        a=datetime.strptime(self.request.data['end'], "%Y-%m-%d")
        b=datetime.strptime(self.request.data['start'],"%Y-%m-%d")
        delta=a-b
        time=delta.days
        
        if len(list(holiday))==0:   #This condition means: "If there is no holiday inside the interval of leave days.
            employee.leave_time-=8*time   #The number of leave hours is reduced by days number times 8, because of the fact that the work day lasts 8 hours. 
            if employee.leave_time<0: #This condition prevents the exceeding of leave time remaining.
                return Response("Attention! You have exceeded the remaining leave time!", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            elif employee.leave_time>=0:
                employee.save()
        
        if len(list(holiday))!=0:  #On the contrary, this means: "If there is holiday inside the interval of leave days". 
            employee.leave_time-=(8*time - 8*len(list(holiday)))   #The official holidays are excluded from the leave, so the hours of those days are substracted from the total hours of all the leave period. are sZbriten dita/et e pushimit zyrtar(pra 8-orarshi/et) nga oret e konsumuara te lejes nga totali
            if employee.leave_time<0:
                return Response("Attention! You have exceeded the remaining leave time!",  status=status.HTTP_405_METHOD_NOT_ALLOWED)
            elif employee.leave_time>=0:
                employee.save()
                 
                
    
    def leave_update_holiday_conditions(self):  #This function is dedicated to the compensation of hours of the leave that the employee wants to cancel. The name of function is like that because of below conditions, which are very important.
        leave=Leave.objects.get(employee=self.request.data['employee'],id=self.kwargs['pk'])
        holiday=Holiday.objects.filter(leave=leave)
        employee=Employee.objects.get(emp_no=self.request.data['employee'])
        
        #Start and end dates of the leave have to converted to datetime objects, so that the number of days can be calculated.  
        c=datetime.strptime(self.request.data['end'], "%Y-%m-%d")
        d=datetime.strptime(self.request.data['start'],"%Y-%m-%d")
        delta=c-d
        time=delta.days
        
        if len(list(holiday))==0:  #This condition is the same as the one at line 76.
            employee.leave_time+=8*time  #Here, differently from the same condition at the function above, the number of hours is added.
            employee.save()
            
        if len(list(holiday))!=0: #This condition is the same as the one at line 83.
            employee.leave_time+=(8*time - 8*len(list(holiday)))  #Here, the number of hours is added, too.
            employee.save()
             
            