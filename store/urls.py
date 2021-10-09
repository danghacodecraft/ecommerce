from django.urls import path
from store.views import *


app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('danh-muc/<str:slug>/', product_list, name='product_list'),
    path('san-pham/<int:pk>/', product_detail, name='product_detail'),
    path('lien-he/', contact, name='contact'),
    path('tim-kiem/', search, name='search'),
]
