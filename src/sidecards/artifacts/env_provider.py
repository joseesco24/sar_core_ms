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

__all__: list[str] = ["EnvProvider"]

load_dotenv(override=True, verbose=True, dotenv_path=find_dotenv(".env"))


class EnvironmentMode(str, Enum):
    development: str = "development"
    production: str = "production"
    testing: str = "testing"


class LoggingMode(str, Enum):
    structured: str = "structured"
    pretty: str = "pretty"


class EnvProvider(BaseSettings):
    # ** info: app configs
    app_environment_mode: EnvironmentMode = Field(..., validation_alias="APP_ENVIRONMENT_MODE")
    app_logging_mode: LoggingMode = Field(..., validation_alias="APP_LOGGING_MODE")
    app_server_port: int = Field(..., validation_alias="APP_SERVER_PORT")
    app_authentication_handler_middleware_exclude: Set[str] = Field(..., validation_alias="APP_AUTHENTICATION_HANDLER_MIDDLEWARE_EXCLUDE")
    app_use_authentication_handler_middleware: bool = Field(..., validation_alias="APP_USE_AUTHENTICATION_HANDLER_MIDDLEWARE")
    app_swagger_docs: bool = Field(..., validation_alias="APP_SWAGGER_DOCS")

    # ** info: users database credentials
    database_password: str = Field(..., validation_alias="DATABASE_PASSWORD")
    database_logs: bool = Field(..., validation_alias="DATABASE_LOGS")
    database_host: str = Field(..., validation_alias="DATABASE_HOST")
    database_name: str = Field(..., validation_alias="DATABASE_NAME")
    database_user: str = Field(..., validation_alias="DATABASE_USER")
    database_port: int = Field(..., validation_alias="DATABASE_PORT")

    # ** info: external microservices base urls
    sar_brms_base_url: HttpUrl = Field(..., validation_alias="SAR_BRMS_BASE_URL")
