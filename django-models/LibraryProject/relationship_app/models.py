from django.db import models

# مؤلف الكتاب
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# الكتاب
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# المكتبة (بها كتب كثيرة)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


# أمين المكتبة (كل مكتبة لها أمين واحد)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name