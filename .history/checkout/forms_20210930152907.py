from django import forms
from .models import Order


class OrderForm(models.Model):
    username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput())
    
    
    class Meta:
        model = Order
        fields = ['username', 'first_name', 'last_name', 'phone', 'address', 'total']
