from django.contrib.auth import get_user_model
from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=120, min_length=6, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'id': 'usernameField',
            'placeholder': 'Enter your username',
        }
    ))
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'email',
            'class': 'form-control',
            'id': 'emailField',
            'placeholder': 'Enter your email',
        }
    ))
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'passwordField',
            'placeholder': 'Enter password'
        }
    ))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'passwordField2',
            'placeholder': 'Confirm password'
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if get_user_model().objects.filter(username=username).exists():
            self.add_error('username', 'Username is taken')

        if not username.isalnum():
            self.add_error('username', 'Username must only be letters!')

        if get_user_model().objects.filter(email=email).exists():
            self.add_error('email', 'Email is taken')

        if password1 != password2:
            self.add_error('password2', 'Passwords do not match!')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, min_length=6, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'id': 'usernameField',
            'placeholder': 'Enter your username',
        }
    ))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'passwordField',
            'placeholder': 'Enter password'
        }
    ))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'id': 'formCheck-1',
            'class': 'form-check-input',
            'value': 'yes',
        }
    ))


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'passwordField',
            'placeholder': 'Enter new password'
        }
    ))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'passwordField2',
            'placeholder': 'Confirm password'
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', 'Passwords do not match!')
