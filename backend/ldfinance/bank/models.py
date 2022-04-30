from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone


# TODO: Move to a model manager?
def _amount_sum_from_past_hour(transaction_queryset):
    one_hour_ago = timezone.now() - timedelta(hours=1)
    return (transaction_queryset
        .filter(created_at__gte=one_hour_ago)
        .aggregate(amount_sum=Coalesce(
            models.Sum("amount"),
            0.0,
            output_field=models.DecimalField(max_digits=12, decimal_places=2),
        ))["amount_sum"]
    )


class Account(models.Model):
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default="0.00")
    is_internal = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def transactions(self):
        return Transaction.objects.filter(
            models.Q(source=self) | models.Q(destination=self)
        ).order_by("-created_at")[:50]

    def deposits_in_past_hour(self):
        return _amount_sum_from_past_hour(self.incoming_transactions)

    def withdrawals_in_past_hour(self):
        return _amount_sum_from_past_hour(self.outgoing_transactions)

    def make_staff_deposit(self, request, amount, description):
        source, _ = Account.objects.get_or_create(name="Staff", is_internal=True)
        destination = self

        account_transactions = Transaction.objects.create(
            created_by=request.user,
            source=source,
            destination=destination,
            amount=amount,
            description=description,
        )
        destination.balance += amount
        destination.save()


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    source = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="outgoing_transactions"
    )
    destination = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="incoming_transactions"
    )

    description = models.TextField()
