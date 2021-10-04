from django import forms
from .models import Order


class OrderForm(models.Model):
    class Meta:
        model = Order
        fields = ['username', 'first_name', 'last_name', 'phone', 'address', 'total']