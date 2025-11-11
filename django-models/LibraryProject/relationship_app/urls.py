# relationship_app/urls.py
from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # FBV
    path('books/', views.book_list_view, name='book-list'),
    
    # CBV
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]