# !/usr/bin/python3
# type: ignore

# ** info: python imports
from dotenv import load_dotenv
from dotenv import find_dotenv
from enum import Enum

# ** info: typing imports
from typing import Set

# ** info: pydantic imports
from pydantic_settings import BaseSettings
from pydantic import HttpUrl
from pydantic import Field

__all__: list[str] = ["configs"]


class EnvironmentMode(str, Enum):
    development: str = "development"
    production: str = "production"
    testing: str = "testing"


class LoggingMode(str, Enum):
    structured: str = "structured"
    pretty: str = "pretty"


class Configs(BaseSettings):
    # ** info: app configs
    app_environment_mode: EnvironmentMode = Field(..., env="APP_ENVIRONMENT_MODE")
    app_logging_mode: LoggingMode = Field(..., env="APP_LOGGING_MODE")
    app_server_port: int = Field(..., env="APP_SERVER_PORT")
    app_authentication_handler_middleware_exclude: Set[str] = Field(..., env="APP_AUTHENTICATION_HANDLER_MIDDLEWARE_EXCLUDE")
    app_use_authentication_handler_middleware: bool = Field(..., env="APP_USE_AUTHENTICATION_HANDLER_MIDDLEWARE")
    app_swagger_docs: bool = Field(..., env="APP_SWAGGER_DOCS")

    # ** info: users database credentials
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    database_logs: bool = Field(..., env="DATABASE_LOGS")
    database_host: str = Field(..., env="DATABASE_HOST")
    database_name: str = Field(..., env="DATABASE_NAME")
    database_user: str = Field(..., env="DATABASE_USER")
    database_port: int = Field(..., env="DATABASE_PORT")

    # ** info: external microservices base urls
    sar_brms_base_url: HttpUrl = Field(..., env="SAR_BRMS_BASE_URL")


load_dotenv(override=True, verbose=True, dotenv_path=find_dotenv(".env"))
configs: Configs = Configs()
