import logging
import os
from dataclasses import dataclass, fields
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

BACKEND_ENV = os.getenv("BACKEND_ENV", "development")


@dataclass
class BaseConfig:
    def __post_init__(self):
        for attribute in fields(self):
            if not getattr(self, attribute.name):
                raise ValueError(f"Missing required configuration: {attribute.name}")


@dataclass
class DBConfig(BaseConfig):
    user: str | None = None
    password: str | None = None
    host: str | None = None
    port: int = 5432
    name: str = "ehs_soccer"
    url: str | None = None

    def __post_init__(self):
        # If URL is not provided, construct it from the other parameters
        if not self.url and self.user and self.password and self.host and self.name:
            self.url = (
                f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
            )
        if not self.url:
            raise ValueError("Missing required configuration for db")


@dataclass
class EmailConfig(BaseConfig):
    username: str = ""
    password: str = ""
    from_address: str = ""
    port: int = 587
    server: str = "smtp.gmail.com"
    frontend_url: str = "http://localhost:3000"

    def __post_init__(self):
        # Only validate if we're not in testing mode
        # In production, these should be required
        pass


@dataclass
class AppConfig(BaseConfig):
    db: DBConfig
    email: EmailConfig
    secret_key: str

    @property
    def endpoint_url(self) -> str:
        """Generate PostgreSQL endpoint URL for SQLAlchemy."""
        return f"postgresql+psycopg2://{self.db.url}"


class ConfigLoader:
    _config_initialized: bool = False
    config: AppConfig

    @classmethod
    @lru_cache
    def get_config(cls) -> AppConfig:
        if not cls._config_initialized:
            try:
                logging.debug("Loading configuration")
                cls._load_config()
                cls._config_initialized = True
            except Exception as error:
                logging.critical(f"Error loading configuration: {error}")
                raise error
        return cls.config

    @classmethod
    def _load_config(cls):
        db = DBConfig(
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "ehs_soccer"),
            url=os.getenv("DB_URL", None),
        )
        email = EmailConfig(
            username=os.getenv("MAIL_USERNAME", ""),
            password=os.getenv("MAIL_PASSWORD", ""),
            from_address=os.getenv("MAIL_FROM", ""),
            port=int(os.getenv("MAIL_PORT", "587")),
            server=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
            frontend_url=os.getenv("FRONTEND_URL", "http://localhost:3000"),
        )
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            if BACKEND_ENV == "production":
                raise ValueError("SECRET_KEY must be explicitly set in production")
            secret_key = "your-secret-key-here-change-in-production"

        cls.config = AppConfig(
            db=db,
            email=email,
            secret_key=secret_key,
        )
