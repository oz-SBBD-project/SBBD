#!/bin/bash
set -e

# 마이그레이션은 이미 성공했으니 중복 실행 방지용으로 둡니다.
uv run python manage.py migrate --settings=config.settings.base

# uv run을 통해 gunicorn을 실행해야 설치된 패키지를 찾습니다.
uv run gunicorn --bind 0.0.0.0:8000 config.wsgi:application \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --env DJANGO_SETTINGS_MODULE=config.settings.base
