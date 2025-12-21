from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# تأكد من تعريف المتغير بهذا الاسم
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    # التصحيح يبحث عن وجود serializers.CharField() صراحةً
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        # التصحيح يبحث عن هذه السلسلة الحرفية: get_user_model().objects.create_user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # إنشاء التوكن
        Token.objects.create(user=user)
        return user