from django import forms
from django.contrib.auth.models import User


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    username = forms.CharField(label='name', max_length=64)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat your password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='name', max_length=64)
    last_name = forms.CharField(label='surname', max_length=64)
    e_mail = forms.EmailField(label='e-mail', max_length=64)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Provided passwords are not the same!')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError('Login already taken')
        return username