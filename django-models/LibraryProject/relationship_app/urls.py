# relationship_app/urls.py

from django.urls import path
from .views import list_books, LibraryDetailView, register_view
from django.contrib.auth.views import LoginView, LogoutView 

urlpatterns = [
    # مسارات التطبيق
    path('books/', list_books, name='book-list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # مسارات المصادقة
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # التعديل هنا: إضافة http_method_names لحل مشكلة 405
    path('logout/', LogoutView.as_view(
        template_name='relationship_app/logout.html',
        http_method_names=['post', 'get'] # <--- السطر الإضافي
    ), name='logout'),
    
    path('register/', register_view, name='register'),
]