from rest_framework import serializers
from .models import User

# Serializer للتسجيل (Registration)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # نحتاج فقط لـ username و email و password للتسجيل
        fields = ('id', 'username', 'email', 'password', 'bio')
        extra_kwargs = {
            'password': {'write_only': True},
            'bio': {'required': False}, # حقل الـ bio اختياري عند التسجيل
        }

    def create(self, validated_data):
        # إنشاء المستخدم مع تشفير كلمة المرور
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio')
        )
        return user

# Serializer لعرض ملف تعريف المستخدم (Profile)
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count')
        read_only_fields = ('username', 'email') # لمنع التعديل على هذه الحقول عبر هذا الـ Serializer

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
        