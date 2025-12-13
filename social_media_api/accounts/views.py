
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import CustomUser

# 1. View لتسجيل المستخدمين الجدد (Registration)
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    # السماح لأي شخص بالوصول (غير مطلوب مصادقة)
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        # إنشاء Token للمستخدم مباشرة بعد التسجيل
        token, created = Token.objects.get_or_create(user=user)
        self.token = token.key

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # إرجاع الـ Token عند النجاح
        response.data['token'] = self.token
        return response

# 2. View لتسجيل الدخول (Login) والحصول على Token
class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        # مصادقة المستخدم
        user = authenticate(username=username, password=password)

        if user is not None:
            # الحصول على Token أو إنشائه
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

# 3. View لعرض وتحديث الملف الشخصي (Profile Management)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # تتطلب مصادقة (IsAuthenticated) لضمان أن المستخدم هو نفسه مالك الملف
    permission_classes = (permissions.IsAuthenticated,) 

    def get_object(self):
        # إرجاع ملف المستخدم الذي قام بتسجيل الدخول حاليًا
        return self.request.user