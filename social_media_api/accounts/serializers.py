from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token 

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        # تأكد من أن 'profile_picture' هو حقل موجود في نموذج المستخدم الخاص بك
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'profile_picture': {'required': False}} # للتأكد من أنه اختياري

    def create(self, validated_data):
        # استخدام .pop() لإزالة الحقول التي لا يجب تمريرها إلى create_user مباشرة إذا لم يكن النموذج الخاص بك يدعمها جميعًا
        password = validated_data.pop('password') 
        
        # إنشاء المستخدم
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=password,
            # يتم تمرير باقي البيانات (bio, profile_picture) كـ kwargs لـ create_user
            **validated_data
        )

        Token.objects.create(user=user)

        return user

# -------------------------------------------------------------
# 2. UserSerializer (مطلوب لـ generics.ListAPIView في accounts/views.py)
# -------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer لعرض بيانات المستخدم الأساسية، يستخدم لـ UserListView ولعرض مؤلف المنشور.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture']

# ملاحظة: يمكنك استخدام UserSerializer في 'posts/serializers.py' 
# لعرض معلومات المؤلف، مما يلغي الحاجة لـ UserDisplaySerializer منفصل.