from rest_framework.test import APITestCase
from rest_framework import status 
from django.urls import reverse
from ,models import Book, Author 
from django.contrib.auth.models import User

class BookAPITest(APITestCase):

    def setUp(self):
        """
        Set up data for testing.
        This runs before every single test method.
        """
        #1. Create a user for authentication testing 
        self.user = User.objects.create_user(username='testuser', password='password')
        
        #2.create an author instance 
        self.author = Author.objects.create(name="J.K. Rowling")

        # 3. Create a book instance
        self.book = Book.objects.create(
            title="Harry Potter",
            publication_year=2001,
            author=self.author
        )

        # 4. Define URLs for easier access
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book.id])
        self.delete_url = reverse('book-delete', args=[self.book.id])

        # 5. Log in the user by default (we will logout manually for permission tests)
        self.client.login(username='testuser', password='password')

    def test_list_books(self):
        """Test retrieving a list of books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We expect at least 1 book (created in setUp)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        """Test retrieving a single book details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter")

    def test_create_book_authenticated(self):
        """Test creating a book with a logged-in user."""
        data = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book_authenticated(self):
        """Test updating a book with a logged-in user."""
        data = {
            "title": "Updated Harry Potter",
            "publication_year": 2001,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db() # Refresh data from DB to check changes
        self.assertEqual(self.book.title, "Updated Harry Potter")

    def test_delete_book_authenticated(self):
        """Test deleting a book with a logged-in user."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_book_unauthenticated(self):
        """Test creating a book WITHOUT logging in (Permission Check)."""
        self.client.logout() # Logout the user explicitly
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        # Should return 403 Forbidden or 401 Unauthorized depending on settings
        # Usually 403 when using IsAuthenticated permissions in views
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book WITHOUT logging in (Permission Check)."""
        self.client.logout()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
       