from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'contacts'

urlpatterns = [
    path('', views.contacts_page, name='contacts_page'),
    path('import_file', views.import_file, name='import_file'),
    path('export_file', views.export_file, name='export_file'),
]
