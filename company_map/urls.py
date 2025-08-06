from django.urls import path
from . import views


app_name = 'company_map'

urlpatterns = [
    path('', views.show, name='map'),
    path('geocode/', views.geocode, name='geocode'),
]
