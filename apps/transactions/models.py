from django.db import models

from apps.accounts.models import Account


class Transaction(models.Model):
    class TxType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "입금"
        WITHDRAW = "WITHDRAW", "출금"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "현금"
        CARD = "CARD", "카드"
        TRANSFER = "TRANSFER", "계좌이체"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    tx_type = models.CharField(max_length=10, choices=TxType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    transaction_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    counterparty = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_id} {self.tx_type} {self.amount}"
