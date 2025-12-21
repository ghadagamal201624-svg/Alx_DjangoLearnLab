from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # إنشاء المستخدم مع تشفير كلمة المرور
        user = CustomUser.objects.create_user(**validated_data)
        # إنشاء Token تلقائياً للمستخدم الجديد
        Token.objects.create(user=user)
        return user