from django.urls import path
from .views import register_user, user_login

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
]