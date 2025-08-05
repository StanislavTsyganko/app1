from django.urls import path
from . import views


app_name = 'employees'

urlpatterns = [
    path('', views.list, name='employees_list'),
    path('generate_test_calls', views.generate_test_calls, name='generate_test_calls'),
]
