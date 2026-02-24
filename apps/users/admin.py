from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "nickname",
        "phone_number",
        "is_staff",
        "is_active",
        "created_at",
    )

    search_fields = (
        "email",
        "nickname",
        "phone_number",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    readonly_fields = ("is_staff",)
