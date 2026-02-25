# apps/analysis/tasks.py
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .analyzers import TransactionAnalyzer

User = get_user_model()


@shared_task
def run_weekly_analysis_all_users():
    """
    모든 유저를 대상으로 지난 일주일간의 데이터를 분석합니다.
    """
    users = User.objects.all()
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    results = []
    for user in users:
        analyzer = TransactionAnalyzer(user, start_date, end_date, period_type="weekly")
        analysis_obj = analyzer.run()
        results.append(analysis_obj.id)

    return f"Created {len(results)} analysis reports."
