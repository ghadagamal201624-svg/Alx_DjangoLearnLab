from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm # تم تصحيح حالة الأحرف (F)
from .models import Book # يجب استيراد Book و النماذج الأخرى

# ------------------------------------
# الـ Views المؤمّنة بالأذونات المخصصة
# ------------------------------------

# 4. View لعرض كتاب (يتطلب إذن 'can_view')
@permission_required('relationship_app.can_view', login_url='/login/')
def secured_book_list_view(request): # تم تصحيح viwe -> view
    all_books = Book.objects.all()
    # تم تصحيح اسم القالب والسياق
    return render(request, 'relationship_app/list_books.html', {'books': all_books}) 

# 5. View لإنشاء كتاب (يتطلب إذن 'can_create')
@permission_required('relationship_app.can_create', raise_exception=True) # تم تصحيح true -> True
def book_create_view(request): # تم تصحيح viwe -> view
    return render(request, 'relationship_app/permission_message.html', {'action': 'Create Book'})

# 6. View لتعديل كتاب (يتطلب إذن 'can_edit')
# يجب إضافة الديكوراتور إذا كانت مؤمنة
@permission_required('relationship_app.can_edit', raise_exception=True) 
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {'action': f'Edit {book.title}'})

# 4. View لحذف كتاب (يتطلب إذن 'can_delete')
@permission_required('relationship_app.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {'action': f'Delete {book.title}'})