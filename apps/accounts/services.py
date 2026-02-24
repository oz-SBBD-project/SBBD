from django.db import transaction as db_transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from .models import Account, Transaction


class TransactionService:
    @staticmethod
    @db_transaction.atomic
    def create_transaction(user, *, account_id, data):
        try:
            account = Account.objects.select_for_update().get(id=account_id, user=user)
        except Account.DoesNotExist:
            raise ValidationError("Account not found")

        tx_type = data["tx_type"]
        amount = data["amount"]

        if tx_type == Transaction.TxType.WITHDRAW:
            if account.balance < amount:
                raise ValidationError("Insufficient balance")
            account.balance = F("balance") - amount
        else:
            account.balance = F("balance") + amount

        account.save(update_fields=["balance", "updated_at"])

        tx = Transaction.objects.create(account=account, **data)
        return tx

    @staticmethod
    @db_transaction.atomic
    def delete_transaction(user, *, tx: Transaction):
        account = Account.objects.select_for_update().get(id=tx.account_id, user=user)

        # reverse balance
        if tx.tx_type == Transaction.TxType.WITHDRAW:
            account.balance = F("balance") + tx.amount
        else:
            account.balance = F("balance") - tx.amount

        account.save(update_fields=["balance", "updated_at"])
        tx.delete()

    @staticmethod
    @db_transaction.atomic
    def update_transaction(user, *, tx: Transaction, data):
        account = Account.objects.select_for_update().get(id=tx.account_id, user=user)

        # 1) revert old
        if tx.tx_type == Transaction.TxType.WITHDRAW:
            account.balance = F("balance") + tx.amount
        else:
            account.balance = F("balance") - tx.amount
        account.save(update_fields=["balance", "updated_at"])
        account.refresh_from_db(fields=["balance"])

        # 2) apply new
        new_type = data.get("tx_type", tx.tx_type)
        new_amount = data.get("amount", tx.amount)

        if new_amount <= 0:
            raise ValidationError("amount must be positive")

        if new_type == Transaction.TxType.WITHDRAW:
            if account.balance < new_amount:
                raise ValidationError("Insufficient balance")
            account.balance = F("balance") - new_amount
        else:
            account.balance = F("balance") + new_amount

        account.save(update_fields=["balance", "updated_at"])

        for k, v in data.items():
            setattr(tx, k, v)
        tx.save()

        return tx
