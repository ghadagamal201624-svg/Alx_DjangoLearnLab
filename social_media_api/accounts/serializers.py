# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# 1. Serializer لتسجيل المستخدمين الجدد
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) # حقل لتأكيد كلمة المرور
    # إضافة حقل Token للقراءة فقط لضمان تواجده في النتيجة
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        # الحقول المطلوبة للتسجيل
        fields = ('username', 'email', 'password', 'password2', 'bio')
        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # إزالة password2 لأنه ليس حقلاً في النموذج
        validated_data.pop('password2') 
        
        # إنشاء المستخدم الجديد
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        token = Token.objects.create(user=user)
        user.token = token.key
        
        return user

# 2. Serializer لعرض وتحديث بيانات الملف الشخصي (Profile)
class UserProfileSerializer(serializers.ModelSerializer):
    # لحساب عدد المتابعين والمتابَعين
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count')
        read_only_fields = ('username', 'email') # لن نسمح بتغيير اسم المستخدم والبريد عبر هذا الـ Serializer

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        # تذكر أننا استخدمنا related_name='following'
        return obj.following.count()