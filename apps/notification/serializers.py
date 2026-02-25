from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """알림(Notification) 모델을 API 응답(JSON)으로 변환"""

    class Meta:
        model = Notification
        # 알림 리스트/읽음처리 응답에 필요한 필드
        fields = ["id", "message", "is_read", "created_at", "analysis"]
        read_only_fields = fields  # 생성/수정은 여기서 받지 않음
