from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.analysis.analyzers import TransactionAnalyzer
from apps.notification.models import Notification

User = get_user_model()


@shared_task
def run_weekly_analysis_all_users():
    users = User.objects.all()
    created_count = 0

    # 1. 일주일치 날짜 계산 (오늘부터 7일 전까지)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    for user in users:
        # 2. 날짜 정보를 포함해서 분석기 인스턴스(객체) 생성!
        try:
            analyzer = TransactionAnalyzer(user, start_date=start_date, end_date=end_date)
            analysis_instance = analyzer.run()

            if analysis_instance:
                Notification.objects.create(
                    user=user,
                    message=f"📊 {user.name}님, {start_date.strftime('%Y-%m-%d')} ~ "
                    f"{end_date.strftime('%Y-%m-%d')} 분석 보고서가 도착했습니다!",
                    is_read=False,
                )
                created_count += 1
        except Exception as e:
            print(f"Error analyzing user {user.name}: {e}")

    return f"Successfully created {created_count} reports and notifications."
