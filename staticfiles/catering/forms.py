from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms
from .models import Menu

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Register as")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class UserLoginForm(AuthenticationForm):
    pass


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'image', 'category']
