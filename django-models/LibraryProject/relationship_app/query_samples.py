# relationship_app/query_samples.py

import os
import django
import sys # إضافة لاستخدامها في طباعة الإخراج

# 1. تهيئة بيئة Django
# تأكدي من استبدال 'django_models.settings' باسم ملف الإعدادات الصحيح لمشروعك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

# استيراد النماذج بعد إعداد البيئة
from relationship_app.models import Author, Book, Library, Librarian


def create_and_test_data():
    """
    ينشئ البيانات المطلوبة وينفذ الاستعلامات، مع إرسال المخرجات
    إلى sys.stdout لضمان التقاطها بواسطة نظام التحقق.
    """
    
    # --- تنظيف البيانات السابقة (اختياري لكن جيد للبيئة التعليمية) ---
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
    
    # المكتبة (OneToOne/ManyToManyField)
    library_main, _ = Library.objects.get_or_create(name='Main City Library')
    
    # أمين المكتبة (OneToOneField)
    librarian_john, _ = Librarian.objects.get_or_create(
        name='John Smith', library=library_main
    )

    # إضافة الكتب إلى المكتبة (ManyToManyField)
    library_main.books.add(book_1, book_3)
    
    # --- 2. الاستعلامات المطلوبة ---
    
    # ====================================================================
    # Task 1: Query all books by a specific author.
    # ====================================================================
    # الهدف: استرجاع جميع كتب 'Ahmed Khaled Tawfik'
    
    # البحث عن المؤلف أولاً
    target_author = Author.objects.get(name='Ahmed Khaled Tawfik')
    
    # الاستعلام: استخدام related_name='books' المعرف في نموذج Author
    author_books = target_author.books.all()
    
    # طباعة النتائج
    sys.stdout.write("Query all books by a specific author:\n")
    for book in author_books:
        sys.stdout.write(f"- {book.title} (Author: {target_author.name})\n")
    
    
    # ====================================================================
    # Task 2: List all books in a library.
    # ====================================================================
    # الهدف: استرجاع جميع الكتب في 'Main City Library'
    
    # البحث عن المكتبة
    target_library = Library.objects.get(name='Main City Library')
    
    # الاستعلام: استخدام ManyToMany field 'books'
    library_books = target_library.books.all()
    
    # طباعة النتائج
    sys.stdout.write("\nList all books in a library:\n")
    for book in library_books:
        sys.stdout.write(f"- {book.title} (Library: {target_library.name})\n")


    # ====================================================================
    # Task 3: Retrieve the librarian for a library.
    # ====================================================================
    # الهدف: استرجاع أمين المكتبة لـ 'Main City Library'
    
    # الاستعلام: استخدام OneToOne field العكسي (الاسم الافتراضي هو اسم النموذج الصغير)
    target_librarian = target_library.librarian
    
    # طباعة النتائج
    sys.stdout.write("\nRetrieve the librarian for a library:\n")
    sys.stdout.write(f"- Librarian Name: {target_librarian.name} (Library: {target_library.name})\n")


if __name__ == '__main__':
    create_and_test_data()
