from django import forms
from .models import 


class OrderForm(models.Model):
    class Meta:
        model = Order