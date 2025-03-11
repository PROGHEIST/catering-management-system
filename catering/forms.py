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


from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }



class EventBookingForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-5 w-5 text-indigo-600 border-gray-300 focus:ring-indigo-500 mr-4'  # Added margin-right to avoid overlap
        }),
        required=True
    )

    class Meta:
        model = EventBooking
        fields = ['event_type', 'event_date', 'venue', 'guest_count','status', 'menu_items']
        widgets = {
            'event_type': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'event_date': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'guest_count': forms.NumberInput(attrs={
                'min': 1,
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(EventBookingForm, self).__init__(*args, **kwargs)
        # Wrap the menu_items in a div container to control its size
        self.fields['menu_items'].widget.attrs['class'] = 'block w-full border-gray-300 focus:ring-indigo-500 rounded-md py-2'
