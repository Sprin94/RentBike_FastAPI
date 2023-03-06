import asyncio

from celery.utils.log import get_task_logger

from app.tasks.celery_app import celery
from app.core.email import send_mail_registration

logger = get_task_logger(__name__)


@celery.task(name="send_email_register")
def task_send_mail_registration(email: str, token: str):
    asyncio.run(send_mail_registration(email, token))
    return True
