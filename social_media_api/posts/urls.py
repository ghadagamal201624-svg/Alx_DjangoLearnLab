from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserFeedView

# إنشاء Router لـ DRF
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # تتضمن جميع المسارات التي تم إنشاؤها بواسطة router (list, create, retrieve, update, destroy)
    path('', include(router.urls)), 
    path('feed/', UserFeedView.as_view(), name='user-feed'),
    
]
