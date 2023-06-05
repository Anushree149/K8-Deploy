
import email
from tkinter import Widget
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter First Name',
        'class':'form-control',
    }))

    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter Last Name',
        'class':'form-control',
    }))

    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter Email',
        'class':'form-control',
    }))
    phone_no=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter Phone Number',
        'class':'form-control',
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_no','email','password','confirm_password']
        # widgets={
        #     first_name=forms.TextInput(attrs={'class':'form-control'})
        # }