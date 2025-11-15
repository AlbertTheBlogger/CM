from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=15)
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    """注册表单"""
    email = forms.EmailField(label='邮箱', min_length=3, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'}))

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):

        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经存在!')
        return email

    def clean_password1(self):

        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data['password1']