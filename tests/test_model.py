from account.models import Account
from django.test import TestCase


class AccountModelTest(TestCase):
    def test_create_model(self, *args: tuple, **kwargs: dict) -> None:
        assert Account.objects.all().count() == 0
        obj: Account = Account.create(email="test@gmail.com")
        obj.save()
        assert Account.objects.all().count() == 1
