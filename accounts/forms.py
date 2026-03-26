from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    
    class Meta:
        model = User
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
        # Apply form-control to all fields, including the password fields from UserCreationForm
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if 'password' in field_name:
                field.widget.attrs['placeholder'] = '••••••••'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'name@example.com'
