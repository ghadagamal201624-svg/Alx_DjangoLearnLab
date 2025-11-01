from bookshelf.models import Book
    
    #Create new book 
    b = Book(title="1984", author="George Orwell", publication_year=1949)
    b.save()
    