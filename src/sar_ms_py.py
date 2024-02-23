# !/usr/bin/python3
# type: ignore

# ** info: python imports
from logging import Logger
from os.path import join
from os import path
import logging
import sys

# ** info: typing imports
from typing import Dict
from typing import Any

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "."))

# ** info: uvicorn imports
import uvicorn

# ** info: fastapi imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi import FastAPI

# ** info: starlette imports
from starlette.middleware.base import BaseHTTPMiddleware

# ** info: rest based routers imports
from src.rest_routers.parameter_router import parameter_router

# ** info: artifacts imports
from src.artifacts.logging.custom_logger import custom_logger
from src.artifacts.path.generator import generator
from src.artifacts.env.configs import configs

# ** info: middlewares imports
from src.middlewares.authentication_handler import authentication_handler
from src.middlewares.logger_contextualizer import logger_contextualizer
from src.middlewares.error_handler import error_handler

# ---------------------------------------------------------------------------------------------------------------------
# ** info: initializing app
# ---------------------------------------------------------------------------------------------------------------------

sar_ms_py: FastAPI = FastAPI()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest base router
# ---------------------------------------------------------------------------------------------------------------------

rest_router: APIRouter = APIRouter(prefix=generator.build_posix_path("rest"))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest routers
# ---------------------------------------------------------------------------------------------------------------------

rest_router.include_router(parameter_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: mounting rest based routers
# ---------------------------------------------------------------------------------------------------------------------

sar_ms_py.include_router(rest_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up global app logging
# ---------------------------------------------------------------------------------------------------------------------

if configs.app_logging_mode == "structured":
    custom_logger.setup_structured_logging()
    logging.info(f"logger setup on {configs.app_logging_mode.lower()} mode")
else:
    custom_logger.setup_pretty_logging()
    logging.info(f"logger setup on {configs.app_logging_mode.lower()} mode")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up app middlewares
# ---------------------------------------------------------------------------------------------------------------------

if configs.app_use_authentication_handler_middleware is True:
    logging.info("authentication middleware active")
    sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=authentication_handler)
else:
    logging.warn("authentication middleware inactive")

sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=error_handler)

sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=logger_contextualizer)

sar_ms_py.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------------------------------------------------------------------------------------------------
# ** info: disabling uvicorn access and error logs on production mode
# ---------------------------------------------------------------------------------------------------------------------

uvicorn_access: Logger = logging.getLogger("uvicorn.access")
uvicorn_error: Logger = logging.getLogger("uvicorn.erro")

if configs.app_environment_mode == "production":
    uvicorn_access.disabled = True
    uvicorn_error.disabled = True
else:
    uvicorn_access.disabled = False
    uvicorn_error.disabled = False

if __name__ == "__main__":
    logging.info(f"application started in {configs.app_environment_mode.lower()} mode")

if __name__ != "__main__":
    logging.info(f"application reloaded in {configs.app_environment_mode.lower()} mode")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up uvicorn asgi server with fast api app
# ---------------------------------------------------------------------------------------------------------------------

uvicorn_server_configs: Dict[str, Any] = {
    "app": sar_ms_py if configs.app_environment_mode == "production" else "sar_ms_py:sar_ms_py",
    "use_colors": False if configs.app_environment_mode == "production" else True,
    "reload": False if configs.app_environment_mode == "production" else True,
    "reload_includes": ["**/*.py", "**/*.graphql"],
    "reload_excludes": ["**/*.pyc", "**/*.pyc.*", "**/*.pyo"],
    "port": configs.app_server_port,
    "log_level": "warning",
    "access_log": False,
    "host": "0.0.0.0",
}

logging.info(f"application starting on port {configs.app_server_port}")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: running app using the previous uvicorn asgi server settings
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(**uvicorn_server_configs)

if configs.app_environment_mode == "production":
    logging.debug("application ended")
