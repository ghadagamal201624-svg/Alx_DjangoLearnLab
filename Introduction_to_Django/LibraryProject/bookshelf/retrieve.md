
# Retrieve the book
    book = Book.objects.get(title="1984")
    # print to check 
    print(book.title, book.author, book.publication_year)