from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
       # رابط عرض كل الكتب
    path('books/', BookListView.as_view(), name='book-list'),

    # رابط عرض تفاصيل كتاب معين باستخدام الـ ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # رابط إنشاء كتاب جديد
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # رابط تحديث كتاب معين
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),

    # رابط حذف كتاب معين
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]