from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserChangeForm):
    email = froms.EmailField(required=True)

    class Meta:
        model = User 
        fields =['username', 'email']
        