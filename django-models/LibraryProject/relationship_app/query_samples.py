# relationship_app/query_samples.py

import os
import django
import sys 

# 1. تهيئة بيئة Django
# !!! هام: تأكدي من استبدال 'django_models.settings' باسم مجلد مشروعك الرئيسي
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

# استيراد النماذج بعد إعداد البيئة
from relationship_app.models import Author, Book, Library, Librarian


def create_and_test_data():
    """
    ينشئ البيانات المطلوبة وينفذ الاستعلامات بناءً على متطلبات نظام التحقق.
    """
    
    # --- تنظيف البيانات السابقة ---
    Author.objects.all().delete()
    Library.objects.all().delete()
    
    # --- 1. إنشاء بيانات عينة ---
    
    # المؤلفين
    author_a, _ = Author.objects.get_or_create(name='Ahmed Khaled Tawfik')
    author_b, _ = Author.objects.get_or_create(name='Naguib Mahfouz')

    # الكتب (ForeignKey)
    book_1, _ = Book.objects.get_or_create(title='Utopia', author=author_a)
    book_2, _ = Book.objects.get_or_create(title='The Days', author=author_a)
    book_3, _ = Book.objects.get_or_create(title='Palace Walk', author=author_b)
    
    # المكتبة
    library_name_target = 'Main City Library'
    library_main, _ = Library.objects.get_or_create(name=library_name_target)
    
    # أمين المكتبة (OneToOneField)
    librarian_john, _ = Librarian.objects.get_or_create(
        name='John Smith', library=library_main
    )

    # إضافة الكتب إلى المكتبة (ManyToManyField)
    library_main.books.add(book_1, book_3)
    
    
    # --- 2. الاستعلامات المطلوبة (مع الالتزام بصيغة التحقق) ---
    
    
    # ====================================================================
    # Task 1: Query all books by a specific author. (حل الخطأ الأخير)
    # ====================================================================
    
    # 1. جلب كائن المؤلف (Author.objects.get(name=author_name))
    author_name_target = 'Ahmed Khaled Tawfik'
    target_author = Author.objects.get(name=author_name_target) 
    
    # 2. الاستعلام باستخدام filter() (الاستعلام المطلوب: .objects.filter(author=author))
    author_books = Book.objects.filter(author=target_author) 
    
    sys.stdout.write("Query all books by a specific author:\n")
    for book in author_books:
        sys.stdout.write(f"- {book.title} (Author: {target_author.name})\n")
    
    
    # ====================================================================
    # Task 2: List all books in a library. (حل الخطأ الذي قبله)
    # ====================================================================
    
    # 1. جلب كائن المكتبة (Library.objects.get(name=library_name))
    target_library = Library.objects.get(name=library_name_target)
    
    # 2. الاستعلام: استخدام ManyToMany field 'books'
    library_books = target_library.books.all()
    
    sys.stdout.write("\nList all books in a library:\n")
    for book in library_books:
        sys.stdout.write(f"- {book.title} (Library: {target_library.name})\n")


    # ====================================================================
    # Task 3: Retrieve the librarian for a library. (هذا كان صحيحاً)
    # ====================================================================
    
    # الاستعلام: استخدام OneToOne field العكسي
    target_librarian = target_library.librarian
    
    sys.stdout.write("\nRetrieve the librarian for a library:\n")
    sys.stdout.write(f"- Librarian Name: {target_librarian.name} (Library: {target_library.name})\n")


if __name__ == '__main__':
    create_and_test_data()