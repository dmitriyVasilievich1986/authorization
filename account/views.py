from rest_framework import viewsets, permissions, exceptions
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import AccountSerializer
from rest_framework import status
from django.utils import timezone
from .models import Account
import json
import re


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        token: str = request.META.get("HTTP_AUTHORIZATION", "")
        substracted_token: str = re.sub(r'^token ', '', token)
        instance: Account = get_object_or_404(Account, token=substracted_token)
        serializer: AccountSerializer = self.get_serializer(instance)
        if serializer.is_token_expired:
            raise exceptions.PermissionDenied
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance: Account = self.get_object()
        serializer: AccountSerializer = self.get_serializer(instance)
        token: str = request.META.get("HTTP_AUTHORIZATION", "")
        if serializer.is_same_token(token) and not serializer.is_token_expired:
            return Response(serializer.data)
        raise exceptions.PermissionDenied

    def create(self, request, *args, **kwargs):
        serializer: AccountSerializer = self.get_serializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers: dict = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        raise exceptions.NotFound

    def destroy(self, request, *args, **kwargs):
        raise exceptions.NotFound

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        data: dict = json.loads(request.body)
        instance: Account = get_object_or_404(Account, email=data.get('email'))
        if not check_password(data.get("password"), instance.password):
            raise exceptions.ValidationError({"password": "wrong password."})
        instance.token_expire = instance.get_token_expire_date()
        instance.token = instance.generate_token()
        instance.save()
        serializer: AccountSerializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def logout(self, request, *args, **kwargs):
        token: str = request.META.get("HTTP_AUTHORIZATION", "")
        substracted_token: str = re.sub(r'^token ', '', token)
        instance: Account = get_object_or_404(Account, token=substracted_token)
        instance.token_expire = timezone.now()
        instance.save()
        return Response("logout")
