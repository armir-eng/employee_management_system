from .models import *
from employees.models import *
from departments.models import *



class UserQueryset: 
    
    def user_queryset_department_manager(self):  #This function gives the right to a user of department manager to get access on data about users of inferior employees of the department he manages and inferior departments. Gets from database all users, belonging to all these employees.
           emp=self.request.user.employee
           manager_employee=Department.objects.filter(dept_manager=emp.emp_no)
           parent_employee=Department.objects.filter(parent=emp.department)
           all_depts=manager_employee | parent_employee
           all_emp=Employee.objects.filter(department__dept_no__in=all_depts)
           user_emp=Users.objects.filter(employee__emp_no__in=all_emp)
           return user_emp
    
    def user_queryset_department_employee(self):  #This means that a user of department employee only has accses to his own data.
           user=self.request.user
           return user

class UserRoleQueryset: #This queryset class defines the right of department managers and department employees on having access on roles of users in system.
    def user_role_queryset_department_manager(self): #A department manager can know the role of only users of employess in department he manages and ones in inferior departments.
           emp=self.request.user.employee
           manager_employee=Department.objects.filter(dept_manager=emp.emp_no)
           parent_employee=Department.objects.filter(parent=emp.department)
           all_depts=manager_employee | parent_employee
           all_emp=Employee.objects.filter(department__dept_no__in=all_depts)
           user_role=UserRole.objects.filter(employee__emp_no__in=all_emp)
           return user_role

    def user_queryset_department_employee(self):  #This means that a user of department employee can only know about his own role.
           user=self.request.user
           user_role=UserRole.objects.filter(user=user)
       