from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


# 토큰 발급
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


# 회원가입
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)


# 로그인
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            response = Response({"access": tokens["access"]}, status=status.HTTP_200_OK)
            response.set_cookie("refresh", tokens["refresh"], httponly=True, samesite="Strict")
            return response
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"detail": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        return response


# 내 정보 조회
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# 정보 수정
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# 회원 탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
