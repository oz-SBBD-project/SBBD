from django.urls import path

from .views import NotificationReadView, UnreadNotificationListView

urlpatterns = [
    # 읽지 않은 알림 목록
    path("unread/", UnreadNotificationListView.as_view(), name="notification-unread"),
    # 알림 읽음 처리
    path("<int:pk>/read/", NotificationReadView.as_view(), name="notification-read"),
]
