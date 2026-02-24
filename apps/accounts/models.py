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
