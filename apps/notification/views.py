from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class UnreadNotificationListView(generics.ListAPIView):
    """
    [미션] 요청한 사용자의 '읽지 않은 알림'만 조회
    GET /notifications/unread/
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 본인 알림 + 안 읽은 것만
        return Notification.objects.filter(user=self.request.user, is_read=False)


class NotificationReadView(APIView):
    """
    [미션] 알림 읽음 처리
    POST /notifications/<pk>/read/
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # 다른 사람 알림은 접근 불가(404)
        notification = get_object_or_404(Notification, pk=pk, user=request.user)

        # 읽음 처리
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        # 처리 결과 반환
        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_200_OK,
        )
