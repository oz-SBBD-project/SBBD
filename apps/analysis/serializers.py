from rest_framework import serializers

from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        # 모델의 모든 칸(필드)을 다 보여주겠다는 뜻입니다.
        fields = "__all__"
