from django.urls import path

from . import views

urlpatterns = [
   
    
    path('holiday/create/', views.HolidayCreate.as_view(), name='create_holiday'),
    path('holiday/list/', views.HolidayList.as_view(), name='list_holiday'),
    path('holiday/<int:pk>/detail/', views.HolidayDetail.as_view(), name='detail_holiday'),
    path('holiday/<int:pk>/update/', views.HolidayUpdate.as_view(), name='update_holiday'),
    path('holiday/<int:pk>/delete/', views.HolidayDelete.as_view(), name='delete_holiday'),

    path('leave/create/', views.LeaveCreate.as_view(), name='create_leave'),
    path('leave/list/', views.LeaveList.as_view(), name='list_leave'),
    path('leave/<int:pk>/detail/', views.LeaveDetail.as_view(), name='detail_leave'),
    path('leave/<int:pk>/update/', views.LeaveUpdate.as_view(), name='update_leave'),
    path('leave/<int:pk>/delete/', views.LeaveDelete.as_view(), name='delete_leave'),

    path('leave/<int:pk>/leave_approval/',views.Leave_Approval.as_view(),name='leave_approval'),
    path('panda/leave/list/',views.LeaveView.as_view(),name='panda'),
    
    ]           
             


