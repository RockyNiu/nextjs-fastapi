from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, SecretStr

from app.config import ConfigLoader


class EmailService:
    def __init__(self):
        config = ConfigLoader.get_config()
        self.conf = ConnectionConfig(
            MAIL_USERNAME=config.email.username,
            MAIL_PASSWORD=SecretStr(config.email.password),
            MAIL_FROM=config.email.from_address,
            MAIL_PORT=config.email.port,
            MAIL_SERVER=config.email.server,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )
        self.frontend_url = config.email.frontend_url
        self.fastmail = FastMail(self.conf)

    async def send_reset_password_email(self, email: EmailStr, token: str) -> None:
        """Send password reset email"""
        reset_url = f"{self.frontend_url}/auth/reset-password?token={token}"

        html = f"""
        <p>Hi,</p>
        <p>You have requested to reset your password. Click the link below to proceed:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>The link will expire in 1 hour.</p>
        """

        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await self.fastmail.send_message(message)

    async def send_verification_email(self, email: EmailStr, token: str) -> None:
        """Send email verification email"""
        verification_url = f"{self.frontend_url}/auth/verify-email?token={token}"

        html = f"""
        <p>Hi,</p>
        <p>Thank you for registering! Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_url}">Verify Email</a></p>
        <p>If you didn't create an account, please ignore this email.</p>
        <p>The link will expire in 24 hours.</p>
        """

        message = MessageSchema(
            subject="Email Verification",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await self.fastmail.send_message(message)
