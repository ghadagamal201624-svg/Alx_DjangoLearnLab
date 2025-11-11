# relationship_app/urls.py

from django.urls import path
from . import views # <-- استيراد شامل
from django.contrib.auth.views import LoginView, LogoutView 
from .views import admin_view, librarian_view, member_view
from .views import add_book_view, edit_book_view, delete_book_view

urlpatterns = [
    # مسارات التطبيق
    # 1. مسار إضافة كتاب (name='add_book' موجود بالفعل)
    path('books/add/', add_book_view, name='add_book'),
    
    # 2. مسار تعديل كتاب (يجب أن يحتوي على edit_book/ في المسار الفعلي)
    path('edit_book/<int:pk>/', edit_book_view, name='edit_book'), # <-- تم التعديل هنا
    
    # 3. مسار حذف كتاب (name='delete_book' موجود بالفعل)
    path('books/delete/<int:pk>/', delete_book_view, name='delete_book'),
    path('books/', views.list_books, name='book-list'), 
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    
    # مسارات المصادقة
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # الالتزام بصيغة التحقق (LogoutView.as_view(template_name=...))
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    
    # الالتزام بصيغة التحقق (views.register_view)
    path('register/', views.register_view, name='register'),

# 1. مسار Admin
    path('admin_area/', admin_view, name='admin_view'),
    
    # 2. مسار Librarian
    path('librarian_area/', librarian_view, name='librarian_view'),
    
    # 3. مسار Member
    path('member_area/', member_view, name='member_view'),
] 


"""# relationship_app/urls.py

from django.urls import path

from . import views # <-- استيراد شامل

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

]"""
