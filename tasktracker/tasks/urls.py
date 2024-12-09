from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),  
    path('task/update-status/<int:pk>/', views.task_update_status, name='task_update_status'),
    path('test_tasks/', views.test_tasks, name='test_tasks'),
]
