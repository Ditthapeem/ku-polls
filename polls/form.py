from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Mata:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

