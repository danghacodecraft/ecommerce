from django import forms
from .models import Order


class OrderForm(models.Model):
    username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username',
    }))

    first_name = forms.CharField(max_length=)
    
    
    class Meta:
        model = Order
        fields = ['username', 'first_name', 'last_name', 'phone', 'address', 'total']
