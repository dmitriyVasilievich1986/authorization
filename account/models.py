from datetime import datetime, timedelta
from django.db import models


class Account(models.Model):
    token_expire = models.DateTimeField(blank=False, null=False)
    email = models.EmailField(verbose_name="email")
    token = models.CharField(
        verbose_name="token",
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )

    @staticmethod
    def get_token_expire_date(*args: list, **kwargs: dict) -> datetime:
        token_expired: datetime = datetime.now() + timedelta(days=1)
        return token_expired
