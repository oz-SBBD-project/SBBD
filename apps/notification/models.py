from django.conf import settings
from django.db import models

from apps.analysis.models import Analysis


class Notification(models.Model):
    """
    사용자에게 전달되는 알림 모델

    - Analysis 생성 시 자동으로 생성됨 (Signal 사용)
    - 사용자는 읽지 않은 알림을 조회 가능
    """

    # 🔹 알림을 받는 사용자 (1:N 관계)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 유저 삭제 시 알림도 삭제
        related_name="notifications",  # user.notifications 로 접근 가능
    )

    # 🔹 어떤 분석으로 인해 생성된 알림인지 (선택)
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.SET_NULL,  # 분석 삭제되어도 알림은 유지
        null=True,
        blank=True,
        related_name="notifications",
    )

    # 🔹 사용자에게 보여줄 알림 메시지
    message = models.TextField()

    # 🔹 읽음 여부 (기본값: False = 안 읽음)
    is_read = models.BooleanField(default=False)

    # 🔹 알림 생성 시각 (자동 저장)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 🔹 최신 알림이 먼저 보이도록 정렬
        ordering = ["-created_at"]

        # 🔹 자주 조회하는 조건(user + is_read)에 인덱스 최적화
        indexes = [
            models.Index(fields=["user", "is_read"]),
        ]

    def __str__(self):
        return f"Notification({self.id}) - User:{self.user_id} - Read:{self.is_read}"
