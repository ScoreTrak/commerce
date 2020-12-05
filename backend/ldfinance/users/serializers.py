from rest_framework import serializers

from ldfinance.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "is_staff",)
