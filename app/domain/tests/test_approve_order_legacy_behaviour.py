from unittest import TestCase

from approvaltests import verify_all_combinations_with_labeled_input

from app.domain.dtos.item import Item
from app.domain.dtos.order import Order
from app.domain.dtos.user import User
from app.domain.appove_order.approve_order import approve_order


class TestApproveOrderLegacyBehaviour(TestCase):
    def test_approve_order(self):
        verify_all_combinations_with_labeled_input(
            self.do_approve_order,
            user_is_premium=[True, False],
            user_is_admin=[True, False],
            user_is_trial=[True, False],
            user_region=["US", "EU"],
            order_amount=[1500, 999],
            order_has_discount=[True, False],
            order_region=["US", "EU"],
            order_currency=["USD", "EUR"],
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

        actual = approve_order(order, user)
        self.assertEqual(expected, actual)

    def do_approve_order(
        self,
        user_is_premium: bool,
        user_is_admin: bool,
        user_is_trial: bool,
        user_region: str,
        order_amount: int,
        order_has_discount: bool,
        order_region: str,
        order_currency: str,
        order_type: str,
    ) -> str:
        user = User(
            is_premium=user_is_premium,
            is_admin=user_is_admin,
            is_trial=user_is_trial,
            region=user_region,
        )

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

        result = approve_order(order, user)
        return f"Order approval result: {result}"
