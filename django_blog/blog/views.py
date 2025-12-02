from django.shortcuts import render, redirect
from django.countrib.auth import login 
from django.countrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages 

#view for registeration 
def register(request):
    if request.method == 'post':
        form = CustomUserCreationForm(request.post)
        if form.is_valid():
            user = form.save()
            login(request, user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form':form})

# view for profile 
@login_required
def profile(request):
    if request.method == 'post':
        user = request.user 
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'profile update successfully')
    return render(request, 'blog/profile.html')

