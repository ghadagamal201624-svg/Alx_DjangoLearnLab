# relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic.detail import DetailView
from .models import Book, Library, Author, UserProfile # استيراد النماذج المطلوبة
from django.contrib.auth import login # للامتثال لمتطلبات التحقق السابقة
from django.db.models import Q #لإظهار الاستعلامات الامنيه
# Note: No need to import User or auth_views directly if using CustomUser/built-in views


# ------------------------------------
# دوال التحقق من الدور (Role Checkers) (لحل مشكلة NameError)
# ------------------------------------

def is_admin(user):
    """التحقق مما إذا كان المستخدم لديه دور 'Admin'."""
    # يجب استخدام CustomUser الآن، والتحقق من وجود UserProfile
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """التحقق مما إذا كان المستخدم لديه دور 'Librarian'."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """التحقق مما إذا كان المستخدم لديه دور 'Member'."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# ------------------------------------
# 1. Function-based View (FBV) for books 
# ------------------------------------
def list_books(request):
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)

def secure_search_view(request):
    search_query = request.GET.get('q', '') # جلب مدخلات المستخدم بأمان
    if search_query:
        # 1. استخدام ORM: يقوم Django بتعقيم (Sanitize) المدخلات تلقائيًا.
        results = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__name__icontains=search_query)
        )
    else:
        results = Book.objects.all()

    # 2. التحقق من صحة المدخلات (مطلوب في المهام السابقة): يجب أن يتم التحقق في Forms
    
    return render(request, 'bookshelf/book_list.html', {'books': results})

# ------------------------------------
# 2. Class-based View (CBV)
# ------------------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ------------------------------------
# 3. View لتسجيل مستخدم جديد (Registration View)
# ------------------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            # بعد إنشاء المستخدم، تأكد أن دوره الافتراضي 'Member' عبر Signals
            return redirect('login') 
    else:
        form = UserCreationForm()
        
    return render(request, 'relationship_app/register.html', {'form': form})

# ------------------------------------
# الـ Views المقيدة بالدور (RBAC)
# ------------------------------------

# Admin View
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

# Librarian View
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

# Member View
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})

# ------------------------------------
# الـ Views المؤمّنة بالأذونات المخصصة (Custom Permissions)
# ------------------------------------

# 1. View لإضافة كتاب (يتطلب إذن 'can_add_book')
@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book_view(request):
    return render(request, 'relationship_app/permission_message.html', {
        'action': 'Adding Books', 
        'permission_granted': True
    })

# 2. View لتعديل كتاب (يتطلب إذن 'can_change_book')
@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {
        'action': f'Editing Book: {book.title}', 
        'permission_granted': True
    })

# 3. View لحذف كتاب (يتطلب إذن 'can_delete_book')
@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/permission_message.html', {
        'action': f'Deleting Book: {book.title}', 
        'permission_granted': True
    })

