from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User


class FormUser(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username",
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email",
    }))
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password",
    }))
    confirm_password = forms.CharField(max_length=100, label='Confirm password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password",
    }))

    class Meta:
        model = User
        fields = '__all__'


class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Portfolio",
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control-file",
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)