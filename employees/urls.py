from django.urls import path

from . import views

urlpatterns=[
    path('employee/create/', views.EmployeeCreate.as_view(), name = 'create_employee'),
    path('employee/list/', views.EmployeeList.as_view(), name = 'list_employee'),
    path('employee/<int:pk>/detail/', views.EmployeeDetail.as_view(), name = 'detail_employee'),
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name = 'update_employee'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name = 'delete_employee'),
]