from celery import shared_task
import logging

logger = logging.getLogger("users")


@shared_task
def send_welcome_email(email):
    logger.info(f"Sending welcome email to {email}")
