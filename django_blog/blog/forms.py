from django import forms 
from .models import Post, comment, tag 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserChangeForm):
    email = froms.EmailField(required=True)

    class Meta:
        model = User 
        fields =['username', 'email']

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas (e.g. tech, django, python)'}))

    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # حفظ التاجز
            tag_names = self.cleaned_data['tags'].split(',')
            for name in tag_names:
                name = name.strip()
                if name:
                    # (احصل عليه إذا كان موجوداً أو أنشئه)
                    tag, created = Tag.objects.get_or_create(name=name)
                    instance.tags.add(tag)
        return instance
           
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'}),
        }
