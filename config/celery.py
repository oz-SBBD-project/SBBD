import os

from celery import Celery

# 장고의 설정 파일 위치를 알려줍니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("SBBD")

# CELERY_로 시작하는 설정들을 가져옵니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# 각 앱 폴더 안에 있는 tasks.py를 비서가 자동으로 읽어갑니다.
app.autodiscover_tasks()
