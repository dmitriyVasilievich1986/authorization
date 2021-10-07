from rest_framework.test import APIClient
from account.models import Account
from django.utils import timezone
from django.test import TestCase
from datetime import timedelta

API_URL = "http://localhost/api/accounts/"


class AccountModelTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        obj: Account = Account.create(email="test1@gmail.com")
        obj.save()
        self.obj_id = obj.id
        self.token = obj.token
        obj2: Account = Account.create(email="test2@gmail.com")
        obj2.token_expire = timezone.now() - timedelta(hours=1)
        obj2.save()
        self.second_id = obj2.id
        self.expired_token = obj2.token
        self.wrong_id = 22

    def test_api_list_wout_credentials(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='wrong token')
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(f'{API_URL}{self.obj_id}/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(f'{API_URL}{self.wrong_id}/')
        self.assertEqual(response.status_code, 404)

    def test_api_list_with_credentials(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')
        response = self.client.get(f'{API_URL}')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'{API_URL}{self.obj_id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'{API_URL}{self.second_id}/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(f'{API_URL}{self.wrong_id}/')
        self.assertEqual(response.status_code, 404)

    def test_api_list_with_expired_credentials(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f'token {self.expired_token}')
        response = self.client.get(f'{API_URL}')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(f'{API_URL}{self.second_id}/')
        self.assertEqual(response.status_code, 403)

    def test_api_update(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f'token {self.token}')
        data = {"email": "newemail@gmail.com"}
        response = self.client.patch(f'{API_URL}{self.obj_id}/', data=data)
        self.assertEqual(response.status_code, 404)
        response = self.client.put(f'{API_URL}{self.obj_id}/', data=data)
        self.assertEqual(response.status_code, 404)

    def test_api_delete(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f'token {self.token}')
        response = self.client.delete(f'{API_URL}{self.obj_id}/')
        self.assertEqual(response.status_code, 404)

    def test_api_retrieve(self, *args: tuple, **kwargs: dict) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')
        url = f'{API_URL}{self.obj_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
