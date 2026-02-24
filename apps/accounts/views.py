from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

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
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # update/partial_update 없음 => "수정 불가" 충족


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.select_related("account")

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

    def destroy(self, request, *args, **kwargs):
        tx = self.get_object()
        TransactionService.delete_transaction(request.user, tx=tx)
        return self.get_response(None, status_code=204)

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
        return self.get_response(out.data, status_code=200)

    # helper
    def get_response(self, data, status_code=200):
        from rest_framework.response import Response

        return Response(data, status=status_code)

    @extend_schema(
        parameters=[
            OpenApiParameter("account_id", OpenApiTypes.INT, required=False),
            OpenApiParameter("tx_type", OpenApiTypes.STR, required=False),
            OpenApiParameter("start_date", OpenApiTypes.DATE, required=False),
            OpenApiParameter("end_date", OpenApiTypes.DATE, required=False),
            OpenApiParameter("min_amount", OpenApiTypes.NUMBER, required=False),
            OpenApiParameter("max_amount", OpenApiTypes.NUMBER, required=False),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
