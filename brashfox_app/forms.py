import datetime

from django import forms
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='Login')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=64, label='Imię')
    email = forms.CharField(label='e-mail', validators=[EmailValidator()])
    topic = forms.CharField(max_length=64, label='Temat')
    message = forms.CharField(widget=forms.Textarea, label='Wiadomość')
    created = forms.DateTimeField(
        widget=forms.HiddenInput,
        initial=datetime.datetime.now(),
        required=False
    )
