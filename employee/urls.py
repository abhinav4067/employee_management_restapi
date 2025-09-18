from django.urls import path
from .views import EmployeeListAPI, EmployeeCreateAPI, EmployeeUpdateAPI, EmployeeDeleteAPI

urlpatterns = [
    path('employees/', EmployeeListAPI.as_view(), name='employee_list_api'),
    path('employees/create/', EmployeeCreateAPI.as_view(), name='employee_create_api'),
    path('employees/update/<int:pk>/', EmployeeUpdateAPI.as_view(), name='employee_update_api'),
    path('employees/delete/<int:pk>/', EmployeeDeleteAPI.as_view(), name='employee_delete_api'),
]
