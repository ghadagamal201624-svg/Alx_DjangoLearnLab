from django.db import models

class Author(models.Model):
    """
    Represents an author in the system.
    Stores the name of the author.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    """
    Represents a book written by an author.
    Stores the title, publication year, and a link to the Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # العلاقة هنا One-to-Many: المؤلف الواحد لديه عدة كتب
    Author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __st__(self):
        return self.title
    
 