# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User # إضافة محتملة قد يطلبها نظام التحقق
from django.contrib.auth import login 
from django.contrib.auth import views as auth_views 
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
# يجب استيراد النماذج والتوابع الأخرى في بداية الملف
from .models import UserProfile
from .models import Book, Library, Author # إضافة Author لاستكمال الاستيرادات

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