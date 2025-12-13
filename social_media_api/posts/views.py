from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

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
# View لجلب موجز التغذية
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # المستخدم الحالي المسجل دخوله
        user = self.request.user
        
        # الحصول على المستخدمين الذين يتابعهم المستخدم الحالي (قائمة بـ IDs)
        following_ids = user.following.values_list('id', flat=True)

        # جلب جميع المنشورات التي تعود للمستخدمين ضمن قائمة following_ids
        # وترتيبها حسب تاريخ الإنشاء تنازليًا (الأحدث أولاً)
        queryset = Post.objects.filter(
            user__id__in=following_ids
        ).order_by('-created_at')

        return queryset