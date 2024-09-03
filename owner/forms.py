from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

# to make password save in hash in admin

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'mobile_no', 'b_date', 'owner_photo')

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'mobile_no', 'b_date', 'owner_photo')