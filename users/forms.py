from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AddUser


class AddUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AddUser
        fields = ('username', 'email', 'job', 'age')


class AddUserChangeForm(UserChangeForm):
    class Meta:
        model = AddUser
        fields = ('username', 'email', 'job', 'age')
