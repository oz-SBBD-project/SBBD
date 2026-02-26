from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
)
from rest_framework import mixins, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import (
    AccountSerializer,
    TransactionCreateSerializer,
    TransactionReadSerializer,
    TransactionUpdateSerializer,
)
from .services import TransactionService


class AccountViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # update/partial_update 없음 => "수정 불가" 충족


class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    # queryset은 get_queryset에서 결정하므로 굳이 클래스 변수로 둘 필요 없음
    # (import 시점 평가 문제도 피함)
    def get_queryset(self):
        qs = Transaction.objects.filter(account__user=self.request.user).select_related("account")

        # --- filters (2개 이상 조건 가능)
        account_id = self.request.query_params.get("account_id")
        tx_type = self.request.query_params.get("tx_type")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        min_amount = self.request.query_params.get("min_amount")
        max_amount = self.request.query_params.get("max_amount")

        if account_id:
            qs = qs.filter(account_id=account_id)
        if tx_type:
            qs = qs.filter(tx_type=tx_type)
        if start_date:
            qs = qs.filter(transaction_date__gte=start_date)
        if end_date:
            qs = qs.filter(transaction_date__lte=end_date)
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)
        if max_amount:
            qs = qs.filter(amount__lte=max_amount)

        return qs.order_by("-transaction_date", "-id")

    def get_serializer_class(self):
        if self.action == "create":
            return TransactionCreateSerializer
        if self.action in ["update", "partial_update"]:
            return TransactionUpdateSerializer
        return TransactionReadSerializer

    # helper
    def get_response(self, data, status_code=200):
        return Response(data, status=status_code)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Transaction Request",
                value={
                    "account_id": 7,
                    "tx_type": "INCOME",
                    "amount": "46542.40",
                    "transaction_date": "2026-02-25",
                    "payment_method": "CASH",
                    "counterparty": "string",
                    "description": "string",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Create Transaction Response",
                value={
                    "id": 1,
                    "account": {
                        "id": 7,
                        "account_name": "string",
                        "account_number": "string",
                        "balance": "46542.40",
                        "created_at": "2026-02-25T17:41:48.598770+09:00",
                        "updated_at": "2026-02-25T17:42:17.031684+09:00",
                    },
                    "tx_type": "INCOME",
                    "amount": "46542.40",
                    "transaction_date": "2026-02-25",
                    "payment_method": "CASH",
                    "counterparty": "string",
                    "description": "string",
                    "created_at": "2026-02-25T17:42:17.034149+09:00",
                    "updated_at": "2026-02-25T17:42:17.034179+09:00",
                },
                response_only=True,
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_id = serializer.validated_data.pop("account_id")
        tx = TransactionService.create_transaction(
            request.user,
            account_id=account_id,
            data=serializer.validated_data,
        )

        out = TransactionReadSerializer(tx, context={"request": request})
        return self.get_response(out.data, status_code=201)

    def partial_update(self, request, *args, **kwargs):
        tx = self.get_object()
        serializer = self.get_serializer(tx, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        tx = TransactionService.update_transaction(
            request.user,
            tx=tx,
            data=serializer.validated_data,
        )

        out = TransactionReadSerializer(tx, context={"request": request})
        return self.get_response(out.data, status_code=201)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="account_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="계좌 ID (예: 7)",
            ),
            OpenApiParameter(
                name="tx_type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="거래 유형 (INCOME 또는 EXPENSE)",
                enum=["INCOME", "EXPENSE"],
            ),
            OpenApiParameter(
                name="start_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="조회 시작 날짜 (형식: YYYY-MM-DD)",
            ),
            OpenApiParameter(
                name="end_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="조회 종료 날짜 (형식: YYYY-MM-DD)",
            ),
            OpenApiParameter(
                name="min_amount",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                required=False,
                description="최소 금액 (예: 10000)",
            ),
            OpenApiParameter(
                name="max_amount",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                required=False,
                description="최대 금액 (예: 50000)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
