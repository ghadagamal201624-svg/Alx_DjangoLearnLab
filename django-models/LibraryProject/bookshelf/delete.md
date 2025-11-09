from bookshelf.models import Book
#Delete the book
    book.delete()
    # print to check
    print(Book.objects.all())