"""User domain exceptions"""


class UserException(Exception):
    """Base exception for user-related errors"""

    pass


class InvalidVerificationTokenError(UserException):
    """Raised when an email verification token is invalid or expired"""

    pass


class EmailAlreadyVerifiedError(UserException):
    """Raised when trying to verify an email that's already verified"""

    pass


class NoVerificationTokenError(UserException):
    """Raised when a user has no verification token"""

    pass


class EmailSendError(UserException):
    """Raised when email sending fails"""

    pass


class UserNotFoundError(UserException):
    """Raised when a user is not found"""

    pass


class UserAlreadyExistsError(UserException):
    """Raised when trying to create a user that already exists"""

    pass


class InvalidCredentialsError(UserException):
    """Raised when login credentials are invalid"""

    pass


class InactiveUserError(UserException):
    """Raised when a user account is inactive"""

    pass


class InvalidPasswordResetTokenError(UserException):
    """Raised when a password reset token is invalid or expired"""

    pass
