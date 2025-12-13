from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# ----------------- Post ViewSet -----------------

class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset لعمليات CRUD لـ Post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # استخدام IsAuthenticatedOrReadOnly لعمليات GET/POST
    # واستخدام IsAuthorOrReadOnly لعمليات PUT/PATCH/DELETE
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 
    
    # الخطوة 5: إضافة Pagination و Filtering
    
    # Pagination يتم إعداده في settings.py، لكن DRF سيطبقه تلقائيًا هنا
    
    # Filtering
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content', 'author__username'] # السماح بالبحث بالعنوان أو المحتوى أو اسم المستخدم للمؤلف

    def perform_create(self, serializer):
        """تعيين المستخدم الحالي كمؤلف عند إنشاء منشور جديد."""
        serializer.save(author=self.request.user)


# ----------------- Comment ViewSet -----------------

class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset لعمليات CRUD لـ Comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # يمكن إضافة تصفية هنا لعرض التعليقات حسب المنشور
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post'] # السماح بالتصفية باستخدام post_id

    def perform_create(self, serializer):
        """تعيين المستخدم الحالي كمؤلف عند إنشاء تعليق جديد."""
        # يمكننا التحقق من وجود 'post' في البيانات المرسلة إذا كنا نريد فرض ذلك
        serializer.save(author=self.request.user)
