from django import forms
from .models import Or


class OrderForm(models.Model):
    class Meta:
        model = Order