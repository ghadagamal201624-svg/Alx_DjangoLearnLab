from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    # المسار: /api/accounts/register
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    
    # المسار: /api/accounts/login
    path('login/', UserLoginView.as_view(), name='user_login'),
    
    # المسار: /api/accounts/profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]