from django import forms
from .models import Order


class OrderForm(models.Model):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username',
    }))

    first_name = forms.CharField(max_length=50, label='first_name', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    
    last_name = forms.CharField(max_length=50, label='last_name', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    phone = forms.CharField(max_length=20, label='Phone number', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    address = forms.CharField(max_length=500, label='Address', widget=forms.)
    
    class Meta:
        model = Order
        fields = ['username', 'first_name', 'last_name', 'phone', 'address', 'total']
