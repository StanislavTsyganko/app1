from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'deals'

urlpatterns = [
    path('', views.list, name='list'),
    path('add', views.add, name='add'),
]
