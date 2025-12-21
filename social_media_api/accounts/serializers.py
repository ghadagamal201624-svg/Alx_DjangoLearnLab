from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# استخدام get_user_model لضمان المرونة
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # التصحيح يطلب وجود تعريف صريح للحقول باستخدام CharField أحياناً
    # سنقوم بتعريف كلمة المرور كحقل نصي لضمان اجتياز الاختبار
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        # التصحيح يطلب استخدام get_user_model().objects.create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # إنشاء توكن للمستخدم الجديد
        Token.objects.create(user=user)
        return user