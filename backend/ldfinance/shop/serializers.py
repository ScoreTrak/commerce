from rest_framework import serializers

from ldfinance.bank.models import Account
from ldfinance.bank.serializers import TransactionSerializer
from ldfinance.shop.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "url", "name", "description", "price", "is_published", "image")

    def get_id(self, obj):
        return str(obj.id)


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    product = ProductSerializer()
    sale = TransactionSerializer()
    refund = TransactionSerializer()

    class Meta:
        model = Order
        # TODO: Separate serializer for internal fields?
        fields = (
            "id", "url", "product", "sale", "refund", "completed_at", # "completed_by"
        )

    def get_id(self, obj):
        return str(obj.id)


class _UserAccountsField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request", None)
        if request is None or not request.user.is_authenticated:
            return None
        if request.user.is_staff:
            return Account.objects.filter(is_internal=False)
        return request.user.account_set.all()


class OrderCreateSerializer(serializers.Serializer):
    account = _UserAccountsField()
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_published=True),
    )
