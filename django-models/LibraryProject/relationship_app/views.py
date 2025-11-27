# relationship_app/views.py
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library
from .models import Book 
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



# 1. Function-based View (FBV) for books 
def list_books(request):
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)

# 2. Class-based View (CBV)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# 3. View لتسجيل مستخدم جديد (Registration View)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # تصحيح الخطأ: يجب أن يكون form.is_valid() وليس forms.valid()
        if form.is_valid(): 
            form.save()
            # بعد التسجيل الناجح، قم بتحويل المستخدم إلى صفحة تسجيل الدخول
            return redirect('login') 
    else:
        form = UserCreationForm()

        
    return render(request, 'relationship_app/register.html', {'form': form})
# relationship_app/views.py (الـ Views الجديدة)

# Admin View
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    # مسار القالب المطلوب للتحقق
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

# Librarian View
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    # مسار القالب المطلوب للتحقق
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

# Member View
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    # مسار القالب المطلوب للتحقق
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})

# 1. View لإضافة كتاب (يتطلب إذن 'can_add_book')
@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book_view(request):
    # في مشروع فعلي، ستحتوي هذه الدالة على منطق نموذج (Form) للإضافة
    return render(request, 'relationship_app/permission_message.html', {
        'action': 'Adding Books', 
        'permission_granted': True
    })

# 2. View لتعديل كتاب (يتطلب إذن 'can_change_book')
@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book_view(request, pk):
    # في مشروع فعلي، ستحتوي هذه الدالة على منطق جلب كتاب وتعديله
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {
        'action': f'Editing Book: {book.title}', 
        'permission_granted': True
    })

# 3. View لحذف كتاب (يتطلب إذن 'can_delete_book')
@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book_view(request, pk):
    # في مشروع فعلي، ستحتوي هذه الدالة على منطق حذف كتاب
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {
        'action': f'Deleting Book: {book.title}', 
        'permission_granted': True
    })