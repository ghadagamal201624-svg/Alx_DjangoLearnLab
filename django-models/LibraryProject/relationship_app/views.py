# relationship_app/urls.py

from django.urls import path
from . import views # <-- استيراد شامل
from django.contrib.auth.views import LoginView, LogoutView 

urlpatterns = [
    # مسارات التطبيق
    path('books/', views.list_books, name='book-list'), 
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    
    # مسارات المصادقة
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # الالتزام بصيغة التحقق (LogoutView.as_view(template_name=...))
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    
    # الالتزام بصيغة التحقق (views.register_view)
    path('register/', views.register_view, name='register'),
]