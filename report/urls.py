from django.urls import path
from .views import html_to_pdf

app_name = 'report'

urlpatterns = [
    path('html-to-pdf/', html_to_pdf, name='html_to_pdf'),
]