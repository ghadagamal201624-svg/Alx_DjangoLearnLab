from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------- Comment Serializers -----------------

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author'] # سيتم تعيين المؤلف تلقائيًا

    def validate(self, data):
        """التحقق من صحة بيانات التعليق"""
        if not data.get('content'):
            raise serializers.ValidationError("محتوى التعليق لا يمكن أن يكون فارغًا.")
        return data

# ----------------- Post Serializers -----------------

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    # حساب عدد التعليقات
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'title', 'content', 
            'created_at', 'updated_at', 'comment_count'
        ]
        read_only_fields = ['author'] # سيتم تعيين المؤلف تلقائيًا

    def get_comment_count(self, obj):
        return obj.comments.count()