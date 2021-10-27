from django.urls import path
from .views import dashboard_with_pivot, pivot_data

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', dashboard_with_pivot, name='dashboard'),
    path('pivot_data/', pivot_data, name='pivot_data')
]