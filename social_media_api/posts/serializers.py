from rest_framework import serializers
from .models import Post
try:
    from ..accounts.models import CustomUser # استيراد نموذج المستخدم المخصص
except ImportError:
    from .accounts.models import CustomUser

# Serializer لعرض معلومات المستخدم بشكل مختصر داخل المنشور
class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True) # لعرض مؤلف المنشور

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']