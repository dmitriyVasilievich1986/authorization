from rest_framework.serializers import ModelSerializer
from datetime import datetime, timedelta
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ['id']

    def create(self, validated_data) -> Account:
        instance: Account = Account.create(**validated_data)
        instance.save()
        return instance

    def is_same_token(self, token: str) -> bool:
        is_same: bool = token == f"token {self.data['token']}"
        return is_same

    @property
    def token_expire_date(self) -> datetime:
        date: datetime = datetime.strptime(
            self.data['token_expire'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return date

    @property
    def is_token_expired(self) -> bool:
        is_expired: bool = self.token_expire_date < datetime.now()
        return is_expired
