from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import *

class UserRegiterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fname','lname','photo','bdate','gender',
                  'city','home_address','phone','is_craftsman']
        
class WorkUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['service', 'description', 'work_from', 'work_to',
                  'price_from', 'price_to', 'work_address',
                  ]

# class SubscriptionForm(forms.Form):
#     accepting_policy = forms.BooleanField(required=False, label='Are You Accepting?')
#     start_date = forms.DateField(required=False, label='Starting date')
#     end

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label='New Email')
    current_password = forms.CharField(widget=forms.PasswordInput, label='Current Password')

class DeleteAccountForm(forms.Form):
    email = forms.EmailField(label='Your email')
    password = forms.CharField(widget=forms.PasswordInput, label='Your Password')


