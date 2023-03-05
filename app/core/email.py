from fastapi_mail import ConnectionConfig, MessageSchema, FastMail

from app.core.config import settings

_conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    TEMPLATE_FOLDER=settings.TEMPLATES_DIR,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

_send_mail = FastMail(_conf)


def _message_config(subject: str, prefix: str, email: str,
                    template_body: dict) -> MessageSchema:
    template_body['url'] = f'http://{settings.HOST}/auth/{prefix}/'
    message = MessageSchema(
        subject=subject,
        recipients=[email, ],
        template_body=template_body,
        subtype="html"
    )
    return message


async def send_mail_registration(email: str, token: str):
    body = {'token': token}
    message = _message_config(
        subject='register', prefix='activation',
        email=email, template_body=body)
    await _send_mail.send_message(
        message=message,
        template_name="email_registration.html")
    return {'detail': True}
