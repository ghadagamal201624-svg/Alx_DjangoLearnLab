# relationship_app/urls.py

from django.urls import path

# يجب استيراد الدالة باسمها الصريح
from .views import list_books, LibraryDetailView 

urlpatterns = [
    # 1. Function-based View (FBV)
    # استخدام اسم الدالة الجديد list_books
    path('books/', list_books, name='book-list'), 

    # 2. Class-based View (CBV)
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]