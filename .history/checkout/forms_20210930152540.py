from django import forms
from .models import Order


class OrderForm(models.Model):
    class Meta:
        model = Order
        fields = []