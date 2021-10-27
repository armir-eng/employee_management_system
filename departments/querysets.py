from .models import *

class DepartmentQueryset:
     def department_queryset_department_manager(self):
            emp=self.request.user.employee #This gets the employee whose user is logged in.
            manager_employee=Department.objects.filter(dept_manager=emp.emp_no)  #This gets the department, whose manager is the logged-in user. 
            parent_employee=Department.objects.filter(parent=emp.dept_manager.dept_no)  #This gets the inferior departments of the above department.
            all_depts=manager_employee | parent_employee  #Merges two querysets above.
            return all_depts
            