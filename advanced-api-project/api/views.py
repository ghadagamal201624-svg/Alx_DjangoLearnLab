from rest_framework import generics 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework

class BookListView(generics.ListAPIView):
    """
    View to list all books.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [filters.OrderingFilter] 
    ordering_fields = '__all__'

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # التحقق من أن المستخدم مسجل دخول


class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

