# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import User

# 

# عرض التسجيل (Registration)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # السماح لأي شخص بالوصول
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # إنشاء الرمز المميز (Token) للمستخدم المسجل حديثاً
        token, created = Token.objects.get_or_create(user=user)

        # الرد بالبيانات والرمز المميز
        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

# عرض تسجيل الدخول (Login)
class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,) # السماح لأي شخص بالوصول

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            # الحصول على الرمز المميز أو إنشائه
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id, "username": user.username})
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# عرض ملف تعريف المستخدم الحالي (Profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,) # يتطلب المصادقة

    def get_object(self):
        # يرجع ملف تعريف المستخدم الذي طلب (المصادق عليه حالياً)
        return self.request.user
