from bookshelf.models import Book
    
    #Create new book 
    b = Book(title="1984", author="George Orwell", publication_year=1949)
    b.save()
    
    # Retrieve the book
    book = Book.objects.get(title="1984")
    # print to check 
    print(book.title, book.author, book.publication_year)
    
    #Update the book title 
    book.title = "Nineteen Eighty-Four"
    book.save()
    # print to check 
    print(book.title)
    
    #Delete the book
    book.delete()
    # print to check
    print(Book.objects.all())
    
    # to exit Shell ---
    exit()