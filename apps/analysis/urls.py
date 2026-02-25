from django.urls import path

from .views import AnalysisListView, AnalysisTriggerView

urlpatterns = [
    # GET /api/analysis/results/ -> 리스트 보기
    path("results/", AnalysisListView.as_view(), name="analysis-list"),
    # POST /api/analysis/trigger/ -> 지금 당장 분석 시작하기
    path("trigger/", AnalysisTriggerView.as_view(), name="analysis-trigger"),
]
