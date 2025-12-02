from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login & Logout (Built-in Views)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # Custom Views
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

