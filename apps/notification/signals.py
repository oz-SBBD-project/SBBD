from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.analysis.models import Analysis

from .models import Notification


@receiver(post_save, sender=Analysis)
def notify_when_analysis_created(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        user=instance.user,
        analysis=instance,
        message="분석이 완료되었습니다. 결과를 확인하세요.",
    )
