from celery import shared_task
import logging
from orders.models import Order

logger = logging.getLogger("orders")


@shared_task
def confirm_order_task(order_id):
    try:
        order = Order.objects.get(id=order_id)
        logger.info(
            f"Task received for Order #{order_id}. Current status: {order.status}"
        )
        order.status = "confirmed"
        order.save()
        logger.info(f"Order #{order_id} status changed to 'confirmed'.")
    except Order.DoesNotExist:
        logger.warning(f"Order #{order_id} not found in confirm_order_task.")
    except Exception as e:
        logger.error(f"Error confirming Order #{order_id}: {e}")
