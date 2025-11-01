from django.db import models

# Create your models here.
class Book(models.Model):
    """
    Represents a Book model with title, author, and publication year.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        # This is optional, but good practice.
        # It shows the book's title in the admin panel instead of "Book object (1)"
        return self.title

