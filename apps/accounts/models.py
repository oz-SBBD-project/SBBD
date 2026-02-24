from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    account_name = models.CharField(max_length=30)
    account_number = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "account_number"],
                name="uniq_user_account_number",
            )
        ]

    def __str__(self):
        return f"{self.user_id}:{self.account_name}"


class Transaction(models.Model):
    class TxType(models.TextChoices):
        INCOME = "INCOME", "수입"
        EXPENSE = "EXPENSE", "지출"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "현금"
        CARD = "CARD", "카드"
        TRANSFER = "TRANSFER", "계좌이체"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    tx_type = models.CharField(max_length=20, choices=TxType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    transaction_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    counterparty = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_id} {self.tx_type} {self.amount}"
