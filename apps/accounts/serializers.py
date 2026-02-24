from rest_framework import serializers

from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_name",
            "account_number",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account_id",
            "tx_type",
            "amount",
            "transaction_date",
            "payment_method",
            "counterparty",
            "description",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["amount"] <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return attrs


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "tx_type",
            "amount",
            "transaction_date",
            "payment_method",
            "counterparty",
            "description",
        ]


class TransactionReadSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "tx_type",
            "amount",
            "transaction_date",
            "payment_method",
            "counterparty",
            "description",
            "created_at",
            "updated_at",
        ]
