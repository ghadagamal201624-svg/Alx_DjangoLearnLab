from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated 
from .models import Post
from .serializers import PostSerializer

# View لجلب موجز التغذية
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        
        following_users = current_user.following.all() 

        queryset = Post.objects.filter(
            
            author__in=following_users 
        ).order_by('-created_at') 
        
        
        return queryset