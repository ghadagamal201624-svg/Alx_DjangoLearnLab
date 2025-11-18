from django.shortcuts import render
from .forms import Exampleform 


#4. View لعرض كتاب (يتطلب إذن 'can_view')
@permission_required('relationship_app.can_view', login_url='/login/')
def secured_book_list_viwe(request):
    all_books = Book.objects.all()
    return render(request, 'relashionship_app/list_book.html', {'books': all:books})

# 5. View لإنشاء كتاب (يتطلب إذن 'can_create')
@permission_required('relationship_app.can_create', raise_exception=true)
def book_create_viwe(request):
    return render(request, 'relationship_app/permission_message.html', {'action': 'Create Book'})

# 6. View لتعديل كتاب (يتطلب إذن 'can_edit')
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {'action': f'Edit {book.title}'})

# 4. View لحذف كتاب (يتطلب إذن 'can_delete')
@permission_required('relationship_app.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {'action': f'Delete {book.title}'})

