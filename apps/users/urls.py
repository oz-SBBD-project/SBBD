from django.urls import path

from .views import LoginView, LogoutView, RegisterView, UserDeleteView, UserMeView, UserUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # 회원가입
    path("login/", LoginView.as_view(), name="login"),  # 로그인
    path("logout/", LogoutView.as_view(), name="logout"),  # 로그아웃
    path("me/", UserMeView.as_view(), name="user-me"),  # 내 정보 조회
    path("me/update/", UserUpdateView.as_view(), name="user-update"),  # 정보 수정
    path("me/delete/", UserDeleteView.as_view(), name="user-delete"),  # 회원 탈퇴
]
