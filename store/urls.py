from django.urls import path
from store.views import *


app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('subcategory/<int:pk>/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
]
