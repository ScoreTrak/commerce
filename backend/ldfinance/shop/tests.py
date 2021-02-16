from decimal import Decimal

from django.urls import reverse
import pytest

from ldfinance.bank.models import Account, Transaction
from ldfinance.shop.models import Answer, Order, Product, Question


@pytest.fixture
def product(db):
    return Product.objects.create(
        name="Test Product",
        description="A product created for testing.",
        price="43.21",
        is_published=True,
        max_per_account=1,
    )


@pytest.fixture
def user_with_account(django_user_model):
    user = django_user_model.objects.create()
    account = Account.objects.create(
        name="Test Account",
        balance="44.44",
    )
    account.users.add(user)
    return user


def test_purchase_succeeds(client, product, user_with_account):
    client.force_login(user_with_account)
    response = client.post(reverse("order-list"), {
        "account": 1,
        "product": product.id,
    })
    assert response.status_code == 201
    account = user_with_account.account_set.first()
    assert account.balance == Decimal("1.23")


def test_purchase_succeeds_with_questions(client, product, user_with_account):
    question1 = Question.objects.create(product=product, text="When?")
    question2 = Question.objects.create(product=product, text="Why?")

    client.force_login(user_with_account)
    response = client.post(reverse("order-list"), {
        "account": 1,
        "product": product.id,
        "challenges": [
            {"question": question2.id, "answer": "Because!"},
            {"question": question1.id, "answer": "Just now."},
        ],
    }, "application/json")
    assert response.status_code == 201
    account = user_with_account.account_set.first()
    assert account.balance == Decimal("1.23")
    assert Answer.objects.count() == 2
    assert Answer.objects.get(order__product=product, question=question1).text == "Just now."
    assert Answer.objects.get(order__product=product, question=question2).text == "Because!"


def test_purchase_fails_account_balance_insufficient(client, product, user_with_account):
    account = user_with_account.account_set.first()
    account.balance = Decimal("33.33")
    account.save()

    client.force_login(user_with_account)
    response = client.post(reverse("order-list"), {
        "account": 1,
        "product": product.id,
    })
    assert response.status_code == 400
    assert response.json() == ['This account has $33.33, but you need $43.21.']
    account = user_with_account.account_set.first()
    assert account.balance == Decimal("33.33")


def test_purchase_fails_max_per_account(client, product, user_with_account):
    Order.objects.create(
        product=product,
        sale=Transaction.objects.create(
            created_by=user_with_account,
            amount="12.34",
            source=user_with_account.account_set.first(),
            destination=Account.objects.create(),
        ),
    )

    client.force_login(user_with_account)
    response = client.post(reverse("order-list"), {
        "account": 1,
        "product": product.id,
    })
    assert response.status_code == 400
    account = user_with_account.account_set.first()
    assert account.balance == Decimal("44.44")
