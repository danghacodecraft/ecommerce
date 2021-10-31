from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('nguoi-ban-hang/', views.users, name='users'),
]