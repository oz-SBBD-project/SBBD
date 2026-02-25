import os

import matplotlib

matplotlib.use("Agg")  # 서버 환경 필수 설정
import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings

from apps.accounts.models import Transaction

from .models import Analysis


class TransactionAnalyzer:
    def __init__(self, user, start_date, end_date, period_type="weekly"):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.period_type = period_type

    def get_data(self):
        queryset = Transaction.objects.filter(
            account__user=self.user, transaction_date__range=[self.start_date, self.end_date]
        ).values("transaction_date", "amount", "tx_type")

        df = pd.DataFrame(list(queryset))

        # [수정 포인트] amount 컬럼을 숫자형태(float)로 강제 변환합니다!
        if not df.empty:
            df["amount"] = df["amount"].astype(float)  # 이 줄을 추가하세요!

        return df

    def visualize(self, df):
        if df.empty:
            return None

        # 날짜별 금액 합계 계산
        summary = df.groupby("transaction_date")["amount"].sum()

        plt.figure(figsize=(10, 6))
        summary.plot(kind="bar", color="skyblue")
        plt.title(f"Spending Analysis ({self.start_date} ~ {self.end_date})")
        plt.xlabel("Date")
        plt.ylabel("Amount")

        # 파일 저장 경로 설정
        file_name = f"analysis_{self.user.id}_{self.start_date}.png"
        relative_path = os.path.join("analysis_results", file_name)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path)
        plt.close()

        return f"{settings.MEDIA_URL}{relative_path}"

    def run(self):
        df = self.get_data()
        image_url = self.visualize(df)

        # Analysis 모델 필드명에 정확히 맞춰서 인스턴스(객체) 생성
        analysis_obj = Analysis.objects.create(
            user=self.user,
            target_type="Total Spending",
            period_type=self.period_type,
            start_date=self.start_date,
            end_date=self.end_date,
            result_image_url=image_url,  # 필드명 수정됨
            status="SUCCESS" if image_url else "FAIL",
            description=f"{self.user.name}님의 {self.period_type} 분석 결과입니다.",
        )
        return analysis_obj
