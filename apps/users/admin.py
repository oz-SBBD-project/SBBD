from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 목록
    list_display = ("id", "email", "nickname", "phone_number", "is_staff", "is_active")

    # 검색
    search_fields = ("email", "nickname", "phone_number")

    # 필터
    list_filter = ("is_staff", "is_active")

    # is_staff 읽기 전용
    readonly_fields = ("is_staff",)

    # username 제거했으니 admin 폼이 꼬이지 않게 fieldsets 조정
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인 정보", {"fields": ("nickname", "name", "phone_number")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("중요 일자", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)

    ordering = ("-date_joined",)
