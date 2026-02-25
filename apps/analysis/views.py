from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Analysis
from .serializers import AnalysisSerializer
from .tasks import run_weekly_analysis_all_users


# 1. 분석 결과 리스트를 보여주는 뷰
class AnalysisListView(generics.ListAPIView):
    """
    사용자의 지출 분석 결과 리스트를 조회합니다.
    """

    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사람만 볼 수 있어요!

    def get_queryset(self):
        # '나(request.user)'의 데이터만 필터링해서 가져와요.
        return Analysis.objects.filter(user=self.request.user).order_by("-created_at")


# 2. (추가 미션용) 수동으로 분석을 실행하는 뷰
class AnalysisTriggerView(APIView):
    """
    POST 요청을 보내면 즉시 주간 분석 비서(Celery Task)를 호출합니다.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 우리가 만든 Celery Task를 비동기로 실행해요!
        run_weekly_analysis_all_users.delay()
        return Response({"message": "분석 작업이 백그라운드에서 시작되었습니다."}, status=status.HTTP_202_ACCEPTED)
