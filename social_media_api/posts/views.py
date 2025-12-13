from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

# View لجلب موجز التغذية
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # المستخدم الحالي المسجل دخوله
        user = self.request.user
        
        # الحصول على IDs المستخدمين الذين يتابعهم المستخدم الحالي
        # هذا يستفيد من العلاقة following في نموذج CustomUser
        following_ids = user.following.values_list('id', flat=True)

        # جلب جميع المنشورات (Posts) التي تعود للمستخدمين ضمن قائمة following_ids
        # وترتيبها حسب تاريخ الإنشاء تنازليًا (الأحدث أولاً)
        queryset = Post.objects.filter(
            user__id__in=following_ids
        ).order_by('-created_at')

        return queryset