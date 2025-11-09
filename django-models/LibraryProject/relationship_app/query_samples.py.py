import os
import django

# إعداد بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# 🧠 1. كل الكتب لمؤلف محدد
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"📚 Books by {author_name}:")
    for book in books:
        print(f"- {book.title}")


# 🧠 2. كل الكتب في مكتبة محددة
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"🏛️ Books in {library_name}:")
    for book in books:
        print(f"- {book.title}")


# 🧠 3. الحصول على أمين المكتبة لمكتبة معينة
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"👩‍💼 Librarian for {library_name}: {librarian.name}")


# ⚙️ تجربة الاستعلامات
if __name__ == "__main__":
    books_by_author("J.K. Rowling")
    books_in_library("Central Library")
    librarian_for_library("Central Library")
