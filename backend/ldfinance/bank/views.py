from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ldfinance.bank.models import Account, Transaction
from ldfinance.bank.serializers import (
    AccountDepositSerializer,
    AccountDepositsSerializer,
    AccountDetailSerializer,
    AccountResetSerializer,
    AccountSerializer,
    CreateAccountAndUserSerializer,
    TransactionSerializer,
)


User = get_user_model()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.none()
    serializer_class = AccountSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Account.objects.filter(is_internal=False)
        else:
            queryset = self.request.user.account_set.all()
        return (queryset
            .prefetch_related("incoming_transactions", "outgoing_transactions")
        )

    def get_serializer_class(self):
        if self.action == "create_with_new_user":
            return CreateAccountAndUserSerializer
        if self.action == "deposit":
            return AccountDepositSerializer
        if self.action == "deposits":
            return AccountDepositsSerializer
        if self.action == "reset":
            return AccountResetSerializer
        if self.action == "retrieve":
            return AccountDetailSerializer
        return AccountSerializer

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def create_with_new_user(self, request):
        assert request.user.is_superuser

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        account_name = serializer.validated_data["account_name"]
        account_balance = serializer.validated_data["account_balance"]
        user = User.objects.create_user(username=username, password=password)
        account = Account.objects.create(name=account_name, balance=account_balance)
        user.account_set.add(account)

        return Response()

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def deposit(self, request, pk=None):
        assert request.user.is_staff  # TODO: Better permission checking.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        description = serializer.validated_data["description"]

        account = Account.objects.select_for_update().get(id=pk)
        account.make_staff_deposit(request, amount, description)

        return Response()  # TODO: Better response.

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def deposits(self, request):
        assert request.user.is_staff  # TODO: Better permission checking.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposits = serializer.validated_data["deposits"]
        description = serializer.validated_data["description"]

        for deposit in deposits:
            account_name = f"Team {deposit['team']}"
            try:
                account = Account.objects.select_for_update().get(name=account_name)
            except Account.DoesNotExist:
                print(f"Account {account_name!r} does not exist")
            else:
                account.make_staff_deposit(request, deposit["amount"], description)

        return Response()  # TODO: Better response.

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def reset(self, request):
        assert request.user.is_superuser  # TODO: Better permission checking.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        balance = serializer.validated_data["balance"]

        accounts = Account.objects.filter(is_internal=False).update(balance=balance)
        transactions = Transaction.objects.all().delete()

        return Response()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.order_by("-created_at").select_related("source", "destination")
