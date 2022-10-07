from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User


class create_user(UserCreationForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields=('username','email','password1','password2','first_name','last_name')
        
class update_data(UserChangeForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields=('username','email')      