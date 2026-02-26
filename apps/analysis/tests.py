import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Analysis

User = get_user_model()


class AnalysisAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="apitester@example.com", password="password123")
        self.client.force_authenticate(user=self.user)

        # 2. 테스트용 분석 데이터 미리 만들어두기
        Analysis.objects.create(
            user=self.user,
            target_type="Spending",
            period_type="weekly",  # 주간 데이터
            start_date=datetime.date(2026, 1, 1),
            end_date=datetime.date(2026, 1, 7),
            status="SUCCESS",
        )
        Analysis.objects.create(
            user=self.user,
            target_type="Spending",
            period_type="monthly",  # 월간 데이터
            start_date=datetime.date(2026, 1, 1),
            end_date=datetime.date(2026, 1, 31),
            status="SUCCESS",
        )

    def test_get_analysis_list(self):
        # 전체 리스트를 잘 가져오는지 확인
        url = reverse("analysis-list")  # urls.py에 설정한 이름
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 데이터가 2개 있어야 함

    def test_filter_analysis_by_period(self):
        # 주간 데이터만 필터링해서 가져오는지 확인
        url = reverse("analysis-list")
        response = self.client.get(url, {"period_type": "weekly"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertGreaterEqual(len(response.data), 1)
        for item in response.data:
            self.assertEqual(item["period_type"], "weekly")
