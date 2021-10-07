from django.test import TestCase, RequestFactory, client
from rest_framework.test import APIRequestFactory, APIClient
from account.models import Account
from account.views import AccountViewSet


class AccountModelTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        obj: Account = Account.create(email="test1@gmail.com")
        obj.save()
        self.obj_id = obj.id
        self.token = obj.token

    def test_create_model(self, *args: tuple, **kwargs: dict) -> None:
        self.assertEqual(Account.objects.all().count(), 1)
        obj: Account = Account.create(email="test@gmail.com")
        obj.save()
        self.assertEqual(Account.objects.all().count(), 2)

    def test_api_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get('http://localhost/api/accounts/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('http://localhost/api/accounts/1/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('http://localhost/api/accounts/2/')
        self.assertEqual(response.status_code, 404)

    def test_api_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')
        url = f'http://localhost/api/accounts/{self.obj_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
