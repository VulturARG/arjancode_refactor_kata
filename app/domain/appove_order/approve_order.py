from app.domain.dtos.order import Order
from app.domain.dtos.user import User


def approve_order(order: Order, user: User) -> str:
    """A tangled, messy function that we’ll clean up in the video."""
    try:
        if user.is_premium:
            if order.amount > 1000:
                if not order.has_discount:
                    if user.region != "EU":
                        for item in order.items:
                            if item.price < 0:
                                return "rejected"
                        return "approved"
                    else:
                        if order.currency == "EUR":
                            return "approved"
                        else:
                            return "rejected"
                else:
                    return "rejected"
            else:
                if order.type == "bulk" and not user.is_trial:
                    return "approved"
                else:
                    return "rejected"
        else:
            if user.is_admin:
                return "approved"
            else:
                return "rejected"
    except Exception:
        # Just to be safe
        return "rejected"
