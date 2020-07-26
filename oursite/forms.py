from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Admission Number',
        widget=forms.TextInput(attrs={'autofocus': True})
    )