from app.domain.dtos.item import Item
from app.domain.dtos.order import Order
from app.domain.dtos.user import User
from app.domain.approve_order.legacy_approve_order import legacy_approve_order


def main() -> None:
    # Create a sample user and order that barely passes the approval rules
    user = User(
        is_premium=True,
        is_admin=False,
        is_trial=False,
        region="US",
    )

    order = Order(
        amount=1500,
        has_discount=False,
        region="EU",
        currency="USD",
        type="normal",
        items=[
            Item("Keyboard", 100.0),
            Item("Monitor", 200.0),
            Item("Mouse", 50.0),
        ],
    )

    result = legacy_approve_order(order, user)
    print(f"Order approval result: {result}")


if __name__ == "__main__":
    main()
