from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'lastname'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your Syrian Virtual University USERNAME'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Syrian Virtual University PASSWORD'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirme your Syrian Virtual University PASSWORD'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','password1','password2'] 

class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your Syrian Virtual University USERNAME'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Syrian Virtual University PASSWORD'}))

class TestMesaageForm(forms.Form):
    message = forms.CharField(error_messages={'required': 'Please enter your message'})

class ChangePasswordForm(forms.Form):
    lastpassword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your current password'}))
    newpassword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your new password'}))