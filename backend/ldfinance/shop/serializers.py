from rest_framework import serializers

from ldfinance.bank.models import Account
from ldfinance.bank.serializers import TransactionSerializer
from ldfinance.shop.models import Answer, Order, Product, Question


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "text")

    def get_id(self, obj):
        return str(obj.id)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    questions = QuestionSerializer(source="question_set", many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "url", "name", "description", "price", "is_published",
            "image", "questions",
        )

    def get_id(self, obj):
        return str(obj.id)


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source="question.text")
    answer = serializers.CharField(source="text")

    class Meta:
        model = Answer
        fields = ("question", "answer")


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    product = ProductSerializer()
    sale = TransactionSerializer()
    refund = TransactionSerializer()
    challenges = AnswerSerializer(source="answer_set", many=True, read_only=True)

    class Meta:
        model = Order
        # TODO: Separate serializer for internal fields?
        fields = (
            "id", "url", "product", "sale", "refund", "completed_at", # "completed_by"
            "challenges",
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


class ChallengeSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.CharField()


class OrderCreateSerializer(serializers.Serializer):
    account = _UserAccountsField()
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_published=True),
    )
    challenges = ChallengeSerializer(many=True, required=False)

    def validate(self, data):
        product = data["product"]
        challenges = data.get("challenges", [])
        expected_qids = {q.id for q in product.question_set.only("id").all()}
        actual_qids = {c["question"].id for c in challenges}
        if expected_qids != actual_qids or len(challenges) != len(expected_qids):
            # TODO: Better error handling.
            raise serializers.ValidationError(
                "All questions must be answered for this order."
            )
        return data
