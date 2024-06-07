import logging
import os
from dataclasses import dataclass, fields
from functools import lru_cache

from dynaconf import Dynaconf

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
BACKEND_ENV = os.getenv("BACKEND_ENV", "development")

settings = Dynaconf(
    envvar_prefix="BACKEND",
    root_path=CONFIG_DIR,
    settings_files=[f"settings.{BACKEND_ENV}.toml", f".secrets.{BACKEND_ENV}.toml"],
)


@dataclass
class BaseConfig:
    def __post_init__(self):
        for attribute in fields(self):
            if not getattr(self, attribute.name):
                raise ValueError(f"Missing required configuration: {attribute.name}")


@dataclass
class MySQLConfig(BaseConfig):
    username: str
    password: str
    host: str
    port: str
    dbname: str


@dataclass
class AppConfig(BaseConfig):
    mysql: MySQLConfig


class ConfigLoader:
    _config_initialized: bool = False
    config: AppConfig

    @classmethod
    @lru_cache
    def get_config(cls) -> AppConfig:
        if not cls._config_initialized:
            try:
                logging.debug("Loading configuration")
                cls._load_config(settings=settings)
                cls._config_initialized = True
            except Exception as error:
                logging.critical(f"Error loading configuration: {error}")
                raise error
        return cls.config

    @classmethod
    def _load_config(cls, settings: Dynaconf):
        mysql = MySQLConfig(
            username=settings.mysql.username,
            password=settings.mysql.password,
            host=settings.mysql.host,
            port=settings.mysql.port,
            dbname=settings.mysql.dbname,
        )
        cls.config = AppConfig(mysql=mysql)
