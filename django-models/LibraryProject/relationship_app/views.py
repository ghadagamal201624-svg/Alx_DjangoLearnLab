# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import views as auth_views 
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from .models import Author

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
