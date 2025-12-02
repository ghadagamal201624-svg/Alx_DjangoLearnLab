from django import forms 
from .models import Post, comment 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserChangeForm):
    email = froms.EmailField(required=True)

    class Meta:
        model = User 
        fields =['username', 'email']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'}),
        }
        