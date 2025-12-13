from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# View Register User
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View Login User
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk
            }, status=status.HTTP_200_OK)
        

# View لمتابعة مستخدم
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # المستخدم الذي يحاول المتابعة
        follower = request.user
        
        # المستخدم المراد متابعته
        try:
            followed = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if follower == followed:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # إضافة المستخدم المراد متابعته إلى قائمة 'following' للمستخدم الحالي
        follower.following.add(followed)


        return Response(
            {"detail": f"Successfully unfollowed user: {unfollowed.username}"},
            status=status.HTTP_200_OK
        )