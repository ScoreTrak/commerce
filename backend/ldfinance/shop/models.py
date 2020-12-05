from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField()
    image = models.URLField(default="https://bank.ubnetdef.org/default-product-image.png")
    # TODO: Add image(s)?
    # TODO: Limit number of purchases for each team?
    # max_per_user = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    # Product being purchased.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Bank transaction for the sale.
    sale = models.OneToOneField(
        "bank.Transaction", on_delete=models.CASCADE, related_name="+"
    )

    # Bank transaction for the refund (only if there was a refund).
    refund = models.OneToOneField(
        "bank.Transaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    # A "completed" order needs no further action.
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
