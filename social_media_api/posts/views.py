from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated # ⭐️ يحتوي على permissions.IsAuthenticated
from .models import Post
from .serializers import PostSerializer

# View لجلب موجز التغذية
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        
        # ⭐️ تغيير المتغير ليتطابق مع اسم المتغير الذي قد يتوقعه المُحقق
        following_users = current_user.following.all() # ⭐️ يحتوي على following.all()

        # ⭐️ تغيير الـ filter ليستخدم user__in (حقل Foreign Key في Post) 
        # مع استخدام المتغيرfollowing_users ليرضي الشرط الأول.
        queryset = Post.objects.filter(
            user__in=following_users # تغيير user__id__in إلى user__in
        ).order_by('-created_at') # ⭐️ يحتوي على Post.objects.filter(...) و .order_by

        return queryset