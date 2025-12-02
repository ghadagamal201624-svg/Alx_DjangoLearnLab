from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.countrib.auth import login 
from django.countrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import Post


# 1. عرض قائمة المنشورات
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date']

# 2. عرض تفاصيل منشور واحد
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# 3. إنشاء منشور جديد (يتطلب تسجيل دخول)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    # تحديد المؤلف تلقائياً قبل الحفظ
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# 4. تحديث منشور (يتطلب تسجيل دخول + أن يكون المستخدم هو المؤلف)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # اختبار للتأكد أن المستخدم هو صاحب المنشور
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# 5. حذف منشور (يتطلب تسجيل دخول + أن يكون المستخدم هو المؤلف)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # التوجيه للصفحة الرئيسية بعد الحذف
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

#view for registeration 
def register(request):
    if request.method == 'post':
        form = CustomUserCreationForm(request.post)
        if form.is_valid():
            user = form.save()
            login(request, user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form':form})

# view for profile 
@login_required
def profile(request):
    if request.method == 'post':
        user = request.user 
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'profile update successfully')
    return render(request, 'blog/profile.html')

