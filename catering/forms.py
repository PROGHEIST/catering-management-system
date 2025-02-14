from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms
from .models import Menu, EventBooking


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




class EventBookingForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border rounded'})
    )
    venue = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Enter Venue'})
    )
    guest_count = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'})
    )
    event_type = forms.ChoiceField(
        choices=EventBooking.EVENT_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )

    class Meta:
        model = EventBooking
        fields = ['event_type', 'event_date', 'venue', 'guest_count']

