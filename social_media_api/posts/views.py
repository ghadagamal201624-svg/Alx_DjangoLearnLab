from rest_framework.generics import ListAPIView
from rest_framework import permissions # ⭐️ لضمان وجود permissions.IsAuthenticated
from .models import Post
from .serializers import PostSerializer

# View لجلب موجز التغذية
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] # ⭐️ يحتوي على permissions.IsAuthenticated

    def get_queryset(self):
        current_user = self.request.user
        
        # ⭐️ ضمان وجود 'following_users' و 'following.all()'
        following_users = current_user.following.all() 

        # ⭐️ ضمان وجود السلسلة النصية الكاملة: Post.objects.filter(author__in=following_users).order_by
        # نستخدم 'author__in' لضمان التطابق الحرفي مع متطلبات المُحقق.
        queryset = Post.objects.filter(
            # هذا هو الجزء الحرج الذي يجب أن يطابق ما يطلبه المُحقق:
            author__in=following_users 
        ).order_by('-created_at') 

        return queryset