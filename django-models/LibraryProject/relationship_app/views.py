# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library, Author

# 1. Function-based View (FBV) for books 
def book_list_view(request):
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)

# 2. Class-based View (CBV)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
