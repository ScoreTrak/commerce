from rest_framework import serializers

from ldfinance.bank.models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = (
            "created_at", "amount", "description", "source", "destination",
        )


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("id", "url", "name", "balance")
        read_only_fields = ("id", "url", "balance")

    def get_id(self, obj):
        return str(obj.id)


class AccountDetailSerializer(AccountSerializer):
    transactions = TransactionSerializer(
        many=True,
        read_only=True,
    )
    deposits_in_past_hour = serializers.DecimalField(max_digits=14, decimal_places=2)
    withdrawals_in_past_hour = serializers.DecimalField(max_digits=14, decimal_places=2)

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + (
            "transactions", "deposits_in_past_hour", "withdrawals_in_past_hour"
        )


class AccountDepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=100)


class _AccountDepositSerializer(serializers.Serializer):
    team = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class AccountDepositsSerializer(serializers.Serializer):
    deposits = _AccountDepositSerializer(many=True)
    description = serializers.CharField(max_length=100)


class AccountResetSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class CreateAccountAndUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(
        trim_whitespace=False, write_only=True, style={"input_type": "password"},
    )
    account_name = serializers.CharField(max_length=20)
    account_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
