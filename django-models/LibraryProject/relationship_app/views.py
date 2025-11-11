# relationship_app/views.py
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from .models import Author

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
