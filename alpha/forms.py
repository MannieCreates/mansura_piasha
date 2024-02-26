from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import login_info, SECURITY_QUESTION_CHOICES


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    age = forms.IntegerField()
    name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    security_question = forms.CharField()
    security_answer = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['security_question'].widget = forms.Select(choices=SECURITY_QUESTION_CHOICES)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ForgotPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    security_answer = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.fields['security_question'].widget = forms.Select(choices=SECURITY_QUESTION_CHOICES)
    # new_password = forms.CharField(widget=forms.PasswordInput())