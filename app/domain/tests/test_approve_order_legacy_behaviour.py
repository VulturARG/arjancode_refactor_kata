from unittest import TestCase

from approvaltests import verify_all_combinations_with_labeled_input

from app.domain.approve_order.approve_order import approve_order
from app.domain.dtos.item import Item
from app.domain.dtos.order import Order
from app.domain.dtos.user import User
from app.domain.approve_order.legacy_approve_order import legacy_approve_order


class TestApproveOrderLegacyBehaviour(TestCase):
    def test_legacy_approve_order(self):
        verify_all_combinations_with_labeled_input(
            self.do_legacy_approve_order,
            user_type=["Admin", "Premium", "Trial"],
            user_region=["US", "EU"],
            order_amount=[1500, 999],
            order_currency=["USD", "EUR"],
            order_has_discount=[True, False],
            order_region=["US", "EU"],
            order_type=["normal", "bulk"],
        )

    def test_approve_order(self):
        verify_all_combinations_with_labeled_input(
            self.do_approve_order,
            user_type=["Admin", "Premium", "Trial"],
            user_region=["US", "EU"],
            order_amount=[1500, 999],
            order_currency=["USD", "EUR"],
            order_has_discount=[True, False],
            order_region=["US", "EU"],
            order_type=["normal", "bulk"],
        )

    def test_user_is_premium_order_amount_greater_1000_order_has_not_discount_user_region_not_eu(
        self,
    ):
        expected = "approved"
        user = User(
            is_premium=True,
            is_admin=False,
            is_trial=False,
            region="US",
        )

        order = Order(
            amount=1500,
            has_discount=False,
            region="US",
            currency="USD",
            type="normal",
            items=[
                Item("Keyboard", 100.0),
            ],
        )

        actual = legacy_approve_order(order, user)
        self.assertEqual(expected, actual)

        actual = approve_order(order, user)
        self.assertEqual(expected, actual)

    def test_user_is_premium_order_amount_greater_1000_order_has_not_discount_user_region_eu(
        self,
    ):
        expected = "approved"
        user = User(
            is_premium=True,
            is_admin=False,
            is_trial=False,
            region="EU",
        )

        order = Order(
            amount=1500,
            has_discount=False,
            region="US",
            currency="EUR",
            type="normal",
            items=[
                Item("Keyboard", 100.0),
            ],
        )

        actual = legacy_approve_order(order, user)
        self.assertEqual(expected, actual)

        actual = approve_order(order, user)
        self.assertEqual(expected, actual)

    def do_legacy_approve_order(
        self,
        user_type: str,
        user_region: str,
        order_amount: int,
        order_currency: str,
        order_has_discount: bool,
        order_region: str,
        order_type: str,
    ) -> str:
        user = self._set_user(user_type=user_type, user_region=user_region)
        order = self._set_order(
            order_amount=order_amount,
            order_currency=order_currency,
            order_has_discount=order_has_discount,
            order_region=order_region,
            order_type=order_type,
        )

        result = legacy_approve_order(order, user)
        return f"Order approval result: {result}"

    def do_approve_order(
        self,
        user_type: str,
        user_region: str,
        order_amount: int,
        order_currency: str,
        order_has_discount: bool,
        order_region: str,
        order_type: str,
    ) -> str:
        user = self._set_user(user_type=user_type, user_region=user_region)
        order = self._set_order(
            order_amount=order_amount,
            order_currency=order_currency,
            order_has_discount=order_has_discount,
            order_region=order_region,
            order_type=order_type,
        )

        result = approve_order(order, user)
        return f"Order approval result: {result}"

    def _set_order(
        self,
        order_amount: int,
        order_currency: str,
        order_has_discount: bool,
        order_region: str,
        order_type: str,
    ) -> Order:
        order = Order(
            amount=order_amount,
            has_discount=order_has_discount,
            region=order_region,
            currency=order_currency,
            type=order_type,
            items=[
                Item("Keyboard", 100.0),
                Item("Monitor", 200.0),
                Item("Mouse", -50.0),
            ],
        )
        return order

    def _set_user(
        self,
        user_type: str,
        user_region: str,
    ) -> User:
        if user_type.lower() == "admin":
            user_is_admin = True
            user_is_premium = False
            user_is_trial = False
        elif user_type.lower() == "premium":
            user_is_admin = False
            user_is_premium = True
            user_is_trial = False
        else:
            user_is_admin = False
            user_is_premium = False
            user_is_trial = True

        user = User(
            is_premium=user_is_premium,
            is_admin=user_is_admin,
            is_trial=user_is_trial,
            region=user_region,
        )
        return user
