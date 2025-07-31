from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'deals'

urlpatterns = [
    path('', views.list, name='deals_list'),
    path('add_deal', views.add, name='add_deal'),
]
