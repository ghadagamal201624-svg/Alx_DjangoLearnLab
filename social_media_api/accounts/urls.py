from django.urls import path
from .views import FollowUserView, UnfollowUserView, register_user, user_login

urlpatterns = [
    # ...
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    # نقاط النهاية الجديدة
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]