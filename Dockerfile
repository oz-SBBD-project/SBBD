FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock /app/
RUN uv sync

COPY . /app

# 1. 베이스 이미지 (3.14-slim 사용)
FROM python:3.14-slim

# 2. 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:$PATH"

# 3. 필수 패키지 설치 및 uv 설치
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 의존성 파일 복사 및 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# 6. 프로젝트 코드 및 스크립트 복사
COPY . .
COPY ./scripts /scripts

# 7. 실행 권한 부여 및 포트 설정
RUN chmod +x /scripts/run.sh
EXPOSE 8000

# 8. run.sh 실행
CMD ["/scripts/run.sh"]