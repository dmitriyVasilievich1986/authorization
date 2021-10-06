from rest_framework.serializers import ModelSerializer
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ['id']

    def create(self, validated_data):
        instance = Account.create(**validated_data)
        instance.save()
        return instance
