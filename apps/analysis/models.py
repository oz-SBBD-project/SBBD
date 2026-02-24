from django.db import models

from config import settings


# 5. Analysis 모델
class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=20)
    period_type = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    result_image_url = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, default="PENDING")
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
