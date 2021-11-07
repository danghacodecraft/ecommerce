from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', index, name='index'),
    path('danh-muc/<str:slug>/', product_list, name='product_list'),
    path('san-pham/<int:pk>/', product_detail, name='product_detail'),
    path('lien-he/', contact, name='contact'),
    path('tim-kiem/', search, name='search'),
    path('rss/', read_rss, name='rss'),
    path('products-service/', products_service, name='products_service'),
    path('product-service/<int:pk>/', product_service, name='product_service'),
]
