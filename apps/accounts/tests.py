from django.test import TestCase
from django.utils import timezone

from apps.users.models import User

from .models import Account, Transaction


# Account Test CRUD
class AccountTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test123@test.com", password="password123")

    # Create (계좌 생성)
    def test_account(self):
        account = Account.objects.create(
            user=self.user, account_name="생활비", account_number="123-456-789", balance=50000
        )
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.account_name, "생활비")

        # Update (계좌 수정)
        account.account_name = "비상금"
        account.save()

        # Read (조회)
        updated_account = Account.objects.get(id=account.id)
        self.assertEqual(updated_account.account_name, "비상금")

        # Delete (삭제)
        updated_account.delete()

        # 삭제 후 데이터 여부 확인
        self.assertEqual(Account.objects.count(), 0)


# Transaction test CRUD
class TransactionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test123@test.com", password="password123")
        self.account = Account.objects.create(user=self.user, account_name="생활비", balance=50000)

    # Create (거래 내역 생성)
    def test_transaction(self):
        tx = Transaction.objects.create(
            account=self.account, amount=10000, transaction_date=timezone.now(), description="용돈"
        )
        self.assertEqual(Transaction.objects.count(), 1)

        # Read (거래 조회)
        saved_tx = Transaction.objects.get(id=tx.id)
        self.assertEqual(saved_tx.amount, 10000)
        self.assertEqual(saved_tx.description, "용돈")
        self.assertEqual(saved_tx.account.account_name, "생활비")

        # Update (거래 수정)
        tx.description = "용돈 입금"
        tx.save()
        self.assertEqual(Transaction.objects.get(id=tx.id).description, "용돈 입금")

        # Delete (거래 삭제)
        tx.delete()
        self.assertEqual(Transaction.objects.count(), 0)
