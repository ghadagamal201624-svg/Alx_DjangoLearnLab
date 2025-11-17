# relationship_app/urls.py

from django.urls import path
from . import views # <-- استيراد شامل
from django.contrib.auth.views import LoginView, LogoutView 
from .views import admin_view, librarian_view, member_view
from .views import add_book_view, edit_book_view, delete_book_view
from .views import secured_book_list_viwe, book_create_view, book_edit_view, book_delete_view

urlpatterns = [
    # مسارات التطبيق
    # 1. مسار إضافة كتاب: يجب أن يحتوي على add_book في السلسلة النصية أو الاسم
    path('add_book/', add_book_view, name='add_book'), # <--- استخدمي هذا المسار بدلاً من 'books/add/'
    
    # 2. مسار تعديل كتاب (حل المشكلة السابقة)
    path('edit_book/<int:pk>/', edit_book_view, name='edit_book'),
    
    # 3. مسار حذف كتاب
    path('delete_book/<int:pk>/', delete_book_view, name='delete_book'),
    
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

    #view
    path('books/secured_list/', secured_book_list_viwe, name='secured_book_list'),

    #create 
    path('books/secure_create/', book_create_view, name='secure_create'),

    #edite
    path('book/secure_edite/<int:pk>/', book_edit_view, name='secure_edit'),

    # Delete
    path('books/secure_delete/<int:pk>/', book_delete_view, name='secure_delete'),


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
