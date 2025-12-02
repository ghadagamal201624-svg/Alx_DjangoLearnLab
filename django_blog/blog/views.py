from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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
from .models import Post, Comment, tag
from django.db.models import Q
from .forms import CommentForm


# 1. إنشاء تعليق جديد
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        # جلب المنشور المرتبط عن طريق الـ ID الموجود في الرابط
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})
    

# 2. تعديل تعليق (لصاحب التعليق فقط)
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    

# 3. حذف تعليق (لصاحب التعليق فقط)
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    


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
    
# 1. البحث (Search View)
def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        # البحث في العنوان أو المحتوى أو اسم التاج
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, 'blog/search_results.html', {'query': query, 'results': results})

# 2. عرض المنشورات حسب التاج (Tag View)
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' # نستخدم نفس قالب القائمة
    context_object_name = 'posts'
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, name=tag_slug)
        return Post.objects.filter(tags=tag).order_by('-published_date')

# تأكد أن PostCreateView و PostUpdateView يستخدمون form_class = PostForm الجديد
# بدلاً من fields = [...]
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm # استخدام الفورم المخصص
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm # استخدام الفورم المخصص
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
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

