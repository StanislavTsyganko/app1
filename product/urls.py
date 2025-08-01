from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'product'

urlpatterns = [
    path('', views.generate_url, name='generate_url'),
    path('product_page/<str:uuid>/', views.product_page, name='product_page'),
]
