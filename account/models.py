from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from typing import Union
from uuid import uuid4


class Account(models.Model):
    token_expire = models.DateTimeField(blank=False, null=False)
    email = models.EmailField(
        verbose_name="email",
        unique=True,
        blank=False,
        null=False,
    )
    token = models.CharField(
        verbose_name="token",
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )

    @classmethod
    def create(cls: models.Model, email: str, *args: tuple, **kwargs: dict) -> models.Model:
        token_expire: datetime = cls.get_token_expire_date()
        token: str = cls.generate_token()
        return cls(email=email, token=token, token_expire=token_expire)

    @staticmethod
    def generate_token(*args: tuple, **kwargs: dict) -> str:
        while True:
            token: str = str(uuid4())
            o: Union[Account, None] = Account.objects.filter(token=token)
            if len(o) == 0:
                break
        return token

    @staticmethod
    def get_token_expire_date(*args: tuple, **kwargs: dict) -> datetime:
        token_expired: datetime = timezone.now() + timedelta(days=1)
        return token_expired
