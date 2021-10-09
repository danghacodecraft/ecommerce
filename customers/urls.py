from django.urls import path
from customers.views import *


app_name = 'customers'
urlpatterns = [
    path('dang-nhap/', login, name='login'),
    path('dang-xuat/', logout, name='logout'),
    path('tai-khoan/', my_account, name='my_account'),
]
