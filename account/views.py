from rest_framework import viewsets, permissions
from .serializer import AccountSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
