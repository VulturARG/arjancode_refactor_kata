from app.domain.dtos.order import Order
from app.domain.dtos.user import User


def is_order_eligible_for_approval(order: Order, user: User) -> bool:
    return order.amount <= 1000 and order.type == "bulk" and not user.is_trial


def is_region_elegible_for_approval(order: Order, user: User) -> bool:
    return user.region == "EU" and order.currency == "EUR"


def approve_order(order: Order, user: User) -> str:
    """A tangled, messy function that we’ll clean up in the video."""
    if user.is_admin:
        return "approved"

    if not user.is_premium:
        return "rejected"

    if is_order_eligible_for_approval(order=order, user=user):
        return "approved"

    if order.amount <= 1000 and order.type != "bulk" or user.is_trial:
        return "rejected"

    if order.has_discount:
        return "rejected"

    if is_region_elegible_for_approval(order=order, user=user):
        return "approved"

    if user.region == "EU" and not order.currency == "EUR":
        return "rejected"

    for item in order.items:
        if item.price < 0:
            return "rejected"

    return "approved"
