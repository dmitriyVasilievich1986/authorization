from django.http import response
from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from .serializer import AccountSerializer
from rest_framework import status
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        raise exceptions.NotFound

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.META.get("HTTP_AUTHORIZATION", "") == f"token {serializer.data['token']}":
            return Response(serializer.data)
        raise exceptions.PermissionDenied

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
