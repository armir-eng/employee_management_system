from django.urls import path

from . import views

urlpatterns = [   
    path('department/create/', views.DepartmentCreate.as_view(), name = 'create_departamen'),
    path('department/list/', views.DepartmentList.as_view(), name = 'list_departament'),
    path('department/<int:pk>/detail/', views.DepartmentDetail.as_view(), name = 'detail_departament'),
    path('department/<int:pk>/update/', views.DepartmentUpdate.as_view(), name = 'update_departament'),
    path('department/<int:pk>/delete/', views.DepartmentDelete.as_view(), name = 'delete_departament'),
]