from django.db import transaction
from django.utils import timezone
from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response

from ldfinance.bank.models import Account, Transaction
from ldfinance.shop.models import Order, Product
from ldfinance.shop.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.none()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.method in SAFE_METHODS
            or view.action == "create"
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or obj.sale.source.filter(users=request.user).exists()
        )


class OrderViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (OrderPermission,)
    queryset = Order.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        if self.action in ("complete", "refund"):
            # No data needed.
            return serializers.Serializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(
                sale__source__in=self.request.user.account_set.all())
        return (queryset
            .select_related(
                "product",
                "sale", "sale__source", "sale__destination",
                "refund", "refund__source", "refund__destination",
            )
            .order_by("-sale__created_at")
        )

    @transaction.atomic
    def perform_create(self, serializer):
        account = serializer.validated_data["account"]
        product = serializer.validated_data["product"]
        # Get the latest data and lock the row.
        account = Account.objects.select_for_update().get(id=account.id)
        if account.balance < product.price:
            raise serializers.ValidationError(
                f"This account has ${account.balance}, but you need ${product.price}."
            )
        account.balance -= product.price
        account.save()
        shop, _ = Account.objects.get_or_create(name="Shop", is_internal=True)
        transaction = Transaction.objects.create(
            created_by=self.request.user,
            amount=-product.price,
            source=account,
            destination=shop,
            description=f"Purchased {product.name!r} from the store",
        )
        Order.objects.create(
            product=product,
            sale=transaction,
        )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def refund(self, request, pk=None):
        # TODO: Auth checks
        assert request.user.is_superuser

        order = self.get_object()

        refund_source = order.sale.destination
        refund_destination = order.sale.source
        refund_amount = -order.sale.amount
        refund_description = f"Refund {order.sale.description}"

        refund_transaction = Transaction.objects.create(
            created_by=request.user,
            amount=refund_amount,
            source=refund_source,
            destination=refund_destination,
            description=refund_description,
        )

        order.refund = refund_transaction
        order.completed_at = timezone.now()
        order.completed_by = request.user
        order.save()

        refund_source.balance -= refund_amount
        refund_source.save()
        refund_destination.balance += refund_amount
        refund_destination.save()
        
        return Response()

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        # TODO: auth checks
        assert request.user.is_superuser

        order = self.get_object()
        order.completed_at = timezone.now()
        order.completed_by = request.user
        order.save()
        return Response()
