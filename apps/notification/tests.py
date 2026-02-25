from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Notification

User = get_user_model()


class NotificationAPITest(APITestCase):
    """
     알림 조회/읽음처리 API 테스트
    - 미확인 알림만 조회되는지
    - 읽음 처리되는지
    - 다른 유저 알림 접근이 막히는지
    """

    def setUp(self):
        # ✅ USERNAME_FIELD=email 커스텀 유저 대응
        self.user1 = User.objects.create(email="u1@test.com")
        self.user1.set_password("pass1234")
        self.user1.save()

        self.user2 = User.objects.create(email="u2@test.com")
        self.user2.set_password("pass1234")
        self.user2.save()

        # user1: unread 1개, read 1개 / user2: unread 1개
        self.n1 = Notification.objects.create(user=self.user1, message="알림1", is_read=False)
        self.n2 = Notification.objects.create(user=self.user1, message="알림2", is_read=True)
        self.n3 = Notification.objects.create(user=self.user2, message="알림3", is_read=False)

    def test_unread_list_returns_only_my_unread(self):
        """내 unread 알림만 조회되는지"""
        self.client.force_authenticate(user=self.user1)

        url = reverse("notification-unread")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], self.n1.id)
        self.assertFalse(res.data[0]["is_read"])

    def test_mark_as_read(self):
        """읽음 처리하면 is_read=True로 바뀌는지"""
        self.client.force_authenticate(user=self.user1)

        url = reverse("notification-read", kwargs={"pk": self.n1.id})
        res = self.client.post(url)

        self.assertEqual(res.status_code, 200)
        self.n1.refresh_from_db()
        self.assertTrue(self.n1.is_read)

    def test_cannot_read_other_users_notification(self):
        """다른 유저 알림은 읽음 처리 불가(404)"""
        self.client.force_authenticate(user=self.user1)

        url = reverse("notification-read", kwargs={"pk": self.n3.id})
        res = self.client.post(url)

        self.assertEqual(res.status_code, 404)
