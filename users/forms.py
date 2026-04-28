from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    # We hide the default username field because we use email
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'role', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add basic CSS classes (optional, but makes it look cleaner)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})