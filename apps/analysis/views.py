from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Analysis
from .serializers import AnalysisSerializer
from .tasks import run_weekly_analysis_all_users


class AnalysisListView(generics.ListAPIView):
    serializer_class = AnalysisSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Analysis.objects.filter(user=self.request.user)

        period_type = self.request.query_params.get("period_type")

        if period_type:
            queryset = queryset.filter(period_type=period_type)

        return queryset.order_by("-created_at")


class AnalysisTriggerView(APIView):
    """
    POST 요청을 보내면 즉시 주간 분석 비서(Celery Task)를 호출합니다.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 우리가 만든 Celery Task를 비동기로 실행해요!
        run_weekly_analysis_all_users.delay()
        return Response({"message": "분석 작업이 백그라운드에서 시작되었습니다."}, status=status.HTTP_202_ACCEPTED)
