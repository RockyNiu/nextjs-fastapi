from unittest.mock import AsyncMock, patch

import pytest
from fastapi_mail import MessageType

from app.service.email_service import EmailService


@pytest.fixture
def email_service():
    """Create an EmailService instance for testing"""
    with patch("app.service.email_service.ConfigLoader.get_config") as mock_config:
        # Mock the configuration
        mock_config.return_value.email.username = "test@example.com"
        mock_config.return_value.email.password = "test_password"
        mock_config.return_value.email.from_address = "test@example.com"
        mock_config.return_value.email.port = 587
        mock_config.return_value.email.server = "smtp.gmail.com"
        mock_config.return_value.email.frontend_url = "http://localhost:3000"

        service = EmailService()
        return service


@pytest.mark.asyncio
async def test_send_reset_password_email(email_service):
    """Test sending reset password email"""
    # Mock the FastMail send_message method
    email_service.fastmail.send_message = AsyncMock()

    test_email = "user@example.com"
    test_token = "test_token_123"

    # Call the method
    await email_service.send_reset_password_email(test_email, test_token)

    # Verify send_message was called once
    email_service.fastmail.send_message.assert_called_once()

    # Get the message that was sent
    call_args = email_service.fastmail.send_message.call_args[0][0]

    # Verify message properties
    assert call_args.subject == "Password Reset Request"
    assert call_args.recipients == [test_email]
    assert "reset-password?token=test_token_123" in call_args.body
    assert call_args.subtype == MessageType.html


@pytest.mark.asyncio
async def test_send_verification_email(email_service):
    """Test sending verification email"""
    # Mock the FastMail send_message method
    email_service.fastmail.send_message = AsyncMock()

    test_email = "user@example.com"
    test_token = "verification_token_123"

    # Call the method
    await email_service.send_verification_email(test_email, test_token)

    # Verify send_message was called once
    email_service.fastmail.send_message.assert_called_once()

    # Get the message that was sent
    call_args = email_service.fastmail.send_message.call_args[0][0]

    # Verify message properties
    assert call_args.subject == "Email Verification"
    assert call_args.recipients == [test_email]
    assert "verify-email?token=verification_token_123" in call_args.body
    assert call_args.subtype == MessageType.html
