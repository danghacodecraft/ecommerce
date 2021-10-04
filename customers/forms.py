from django import forms
from customers import models


class FormDangKy(forms.ModelForm):
    ho = forms.CharField(max_length=250, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Họ"
    }))
    ten = forms.CharField(max_length=250, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Tên"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    mat_khau = forms.CharField(max_length=100, label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu"
    }))
    xac_nhan_mat_khau = forms.CharField(max_length=100, label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Xác nhận Mật khẩu"
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Điện thoại"
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Địa chỉ",
        "rows": 4,
    }))

    class Meta:
        model = models.Customer
        # fields = '__all__'
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']


class FormThongTin(forms.ModelForm):
    ho = forms.CharField(max_length=250, label='Họ:', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Họ",
        "readonly": "readonly",
    }))
    ten = forms.CharField(max_length=250, label='Tên:', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Tên",
        "readonly": "readonly",
    }))
    email = forms.EmailField(label='Email / Tên đăng nhập:', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email",
        "readonly": "readonly",
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại:', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Điện thoại"
    }))
    dia_chi = forms.CharField(label='Địa chỉ:', widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Địa chỉ",
        "rows": 3,
        "style": "resize:none",
    }))

    class Meta:
        model = models.Customer
        fields = ['ho', 'ten', 'email', 'dien_thoai', 'dia_chi']


class FormDoiMatKhau(forms.ModelForm):
    mat_khau = forms.CharField(max_length=100, label='Mật khẩu cũ', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu cũ"
    }))
    mat_khau_moi = forms.CharField(max_length=100, label='Mật khẩu mới', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu mới"
    }))
    xac_nhan_mat_khau = forms.CharField(max_length=100, label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Xác nhận mật khẩu"
    }))

    class Meta:
        model = models.Customer
        fields = ['mat_khau',]
