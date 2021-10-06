from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ['id']
