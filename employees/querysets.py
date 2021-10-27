from .models import *
from departments.models import *
class EmployeeQueryset: 
    
    def employee_queryset_department_manager(self):
        emp=self.request.user.employee #This gets the employee whose user is logged in.
        manager_department=Department.objects.filter(dept_manager=emp.emp_no)  #This gets the department, whose manager is the logged-in user.
        child_departments=Department.objects.filter(parent=emp.dept_manager.dept_no)   #This gets the inferior departments of the above department.
        all_depts=manager_department | child_departments #Merges two querysets above.
        all_emp=Employee.objects.filter(department__dept_no__in=all_depts)   # This gets all employees of the filtered group of departments.
        return all_emp

    
    def employee_queryset_department_employee(self):
        user=self.request.user  #This gets the logged-in user.
        emp=Employee.objects.filter(user=user)   #"This gets only the employee whose user is logged in.
        return emp
