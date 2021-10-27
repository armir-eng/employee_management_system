from django.urls import path

from . import views

urlpatterns= [
    path('users/create/', views.UsersCreate.as_view(), name = 'create_user'),
    path('users/list/', views.UsersList.as_view(), name = 'list_user'),
    path('users/<int:pk>/detail/', views.UsersDetail.as_view(), name = 'detail_user'),
    path('users/<int:pk>/update/', views.UsersUpdate.as_view(), name = 'update_user'),
    path('users/<int:pk>/delete/', views.UsersDelete.as_view(), name = 'delete_user'),

    path('user_role/create/', views.UserRoleCreate.as_view(), name = 'create_user_role'),
    path('user_role/list/', views.UserRoleList.as_view(), name = 'list_user_role'),
    path('user_role/<int:pk>/update/', views.UserRoleUpdate.as_view(), name = 'update_user_role'), 
    path('user_role/<int:pk>/detail/', views.UserRoleDetail.as_view(), name = 'detail_user_role'),
    path('user_role/<int:pk>/delete/',views.UserRoleDelete.as_view(), name = 'delete_user_role'),
    
    path('role/create/', views.RoleCreate.as_view(), name = 'create_role'),
    path('role/list/', views.RoleList.as_view(), name = 'list_role'),
    path('role/<int:pk>/update/', views.RoleUpdate.as_view(), name = 'update_role'),
    path('role/<int:pk>/detail/', views.RoleDetail.as_view(), name='role_detail'),
    path('role/<int:pk>/delete/',views.RoleDelete.as_view(), name = 'delete_role'),


]