from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer # ستحتاج لإنشاء سيريالايزر بسيط له

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.filter(unread=True).order_by('-timestamp')