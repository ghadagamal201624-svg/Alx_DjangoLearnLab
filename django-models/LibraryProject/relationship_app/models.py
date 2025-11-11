# relationship_app/models.py

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# 1. تعريف Book مرة واحدة فقط، ويجب أن يسبق Library
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(default=2000) # تأكدي من وجود هذا الحقل هنا فقط
    def __str__(self):
        return self.title

# 2. تعريف Library (الذي يشير إلى Book)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name

# 3. تعريف Librarian
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Librarian: {self.name} for {self.library.name}"