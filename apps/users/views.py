from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class RegisterResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


# 토큰 발급
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


# 회원가입
@extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterResponseSerializer},
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)


# 로그인
@extend_schema(
    request=LoginRequestSerializer,
    responses={200: LoginResponseSerializer, 401: RegisterResponseSerializer},
)
class LoginView(APIView):
    permission_classes = [AllowAny]

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
@extend_schema(
    request=None,
    responses={200: RegisterResponseSerializer, 400: RegisterResponseSerializer},
)
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
@extend_schema(responses=UserSerializer)
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# 정보 수정
@extend_schema(request=UserSerializer, responses=UserSerializer)
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# 회원 탈퇴
@extend_schema(responses={200: RegisterResponseSerializer})
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
