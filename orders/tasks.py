from celery import shared_task
from orders.models import Order
from utils.telegram import send_telegram_message


@shared_task
def confirm_order_task(order_id):
    try:
        order = (
            Order.objects.select_related("user", "table")
            .prefetch_related("items__dish")
            .get(pk=order_id)
        )
    except Order.DoesNotExist:
        return

    message_lines = [
        f"New order: {order.id}",
        f"Table: {order.table.number}",
        f"Client : {order.user.email}",
        "",
        "Dish:",
    ]

    for item in order.items.all():
        message_lines.append(f"{item.dish.name} quantity {item.quantity}")

    message = "\n".join(message_lines)

    send_telegram_message(message, order_id=order.id)
