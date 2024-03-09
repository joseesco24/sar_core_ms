# !/usr/bin/python3

# ** info: python imports
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
from src.modules.collect_request.ports.rest_routers.collect_request_router import collect_request_router  # type: ignore
from src.modules.parameter.ports.rest_routers.parameter_router import parameter_router
from src.modules.waste.ports.rest_routers.waster_router import waste_router

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.logging_provider import LoggingProvider  # type: ignore
from src.sidecards.artifacts.env_provider import EnvProvider  # type: ignore
from src.sidecards.artifacts.path_provider import PathProvider  # type: ignore

# ** info: sidecard.middlewares imports
from src.sidecards.middlewares.authentication_handler_middleware import AuthenticationHandlerMiddleware  # type: ignore
from src.sidecards.middlewares.logger_contextualizer_middleware import LoggerContextualizerMiddleware  # type: ignore
from src.sidecards.middlewares.error_handler_middleware import ErrorHandlerMiddleware  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building needed artifacts
# ---------------------------------------------------------------------------------------------------------------------

path_provider: PathProvider = PathProvider()
env_provider: EnvProvider = EnvProvider()  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up global app logging
# ---------------------------------------------------------------------------------------------------------------------

if env_provider.app_logging_mode == "structured":
    LoggingProvider.setup_structured_logging()
    logging.info(f"logger setup on {env_provider.app_logging_mode.lower()} mode")
else:
    LoggingProvider.setup_pretty_logging()
    logging.info(f"logger setup on {env_provider.app_logging_mode.lower()} mode")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: initializing app metadata and documentation
# ---------------------------------------------------------------------------------------------------------------------

metadata: Dict[str, Any] = {
    "description": "This repository corresponds to the a small python microservice that is going to be used used in the sar system.",
    "summary": "Service incharge of managing wastes, collect request, and system parameters.",
    "title": "Sar Python Microservice",
    "version": "v2.6.0",
}

sar_ms_py: FastAPI
if env_provider.app_swagger_docs is True:
    sar_ms_py = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1}, redoc_url=None, **metadata)  # type: ignore
    logging.warning("swagger docs active")
else:
    sar_ms_py = FastAPI(docs_url=None, redoc_url=None, **metadata)
    logging.warning("swagger docs inactive")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest base router
# ---------------------------------------------------------------------------------------------------------------------

rest_router: APIRouter = APIRouter(prefix=path_provider.build_posix_path("rest"))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest routers
# ---------------------------------------------------------------------------------------------------------------------

rest_router.include_router(router=collect_request_router)
rest_router.include_router(router=parameter_router)
rest_router.include_router(router=waste_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: mounting rest based routers
# ---------------------------------------------------------------------------------------------------------------------

sar_ms_py.include_router(rest_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up app middlewares
# ---------------------------------------------------------------------------------------------------------------------

if env_provider.app_use_authentication_handler_middleware is True:
    logging.info("authentication middleware active")
    sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=AuthenticationHandlerMiddleware())
else:
    logging.warning("authentication middleware inactive")

sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=ErrorHandlerMiddleware())
sar_ms_py.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=LoggerContextualizerMiddleware())
sar_ms_py.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------------------------------------------------------------------------------------------------
# ** info: hot reload notification
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.info(f"application started in {env_provider.app_environment_mode.lower()} mode")
if __name__ != "__main__":
    logging.info(f"application reloaded in {env_provider.app_environment_mode.lower()} mode")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up uvicorn asgi server with fast api app
# ---------------------------------------------------------------------------------------------------------------------

uvicorn_server_configs: Dict[str, Any] = {
    "app": sar_ms_py if env_provider.app_environment_mode == "production" else "sar_ms_py:sar_ms_py",
    "log_level": "debug" if env_provider.app_environment_mode != "production" else "error",
    "use_colors": False if env_provider.app_environment_mode == "production" else True,
    "reload": False if env_provider.app_environment_mode == "production" else True,
    "reload_excludes": ["**/*.pyc", "**/*.pyc.*", "**/*.pyo"],
    "reload_includes": ["**/*.py", "**/*.graphql"],
    "port": env_provider.app_server_port,
    "access_log": False,
    "host": "0.0.0.0",
}

logging.info(f"application starting on port {env_provider.app_server_port}")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: running app using the previous uvicorn asgi server settings
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(**uvicorn_server_configs)

if env_provider.app_environment_mode == "production":
    logging.debug("application ended")
