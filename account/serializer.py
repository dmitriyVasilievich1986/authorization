from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions
from datetime import datetime
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data) -> Account:
        for field in ["email", "password"]:
            if field not in validated_data:
                message = {field: "The field cannot be empty"}
                raise exceptions.ValidationError(message)
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
