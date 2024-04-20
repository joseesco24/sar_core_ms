# !/usr/bin/python3

# ** info: python imports
from os.path import join
from os import path
import logging
import locale
import sys
import gc

# ** info: typing imports
from typing import List
from typing import Dict
from typing import Any

# ---------------------------------------------------------------------------------------------------------------------
# ** info: appending src path to the system paths for absolute imports from src path
# ---------------------------------------------------------------------------------------------------------------------

sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "."))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: continuing with the app setup
# ---------------------------------------------------------------------------------------------------------------------

# ** info: uvicorn imports
import uvicorn

# ** info: fastapi imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi import FastAPI

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.logging_provider import LoggingProvider  # type: ignore
from src.sidecard.system.artifacts.env_provider import EnvProvider  # type: ignore
from src.sidecard.system.artifacts.path_provider import PathProvider  # type: ignore

# ** info: starlette imports
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import BaseRoute
from starlette.routing import Mount
from starlette.routing import Route

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building needed artifacts
# ---------------------------------------------------------------------------------------------------------------------

path_provider: PathProvider = PathProvider()
env_provider: EnvProvider = EnvProvider()  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up app locale configuration
# ---------------------------------------------------------------------------------------------------------------------

locale.setlocale(category=locale.LC_ALL, locale=env_provider.app_posix_locale)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: continuing with the app setup
# ---------------------------------------------------------------------------------------------------------------------

# ** info: graphql based routers imports
from src.modules.waste.ports.graphql_routers.waste_router import waste_gpl_router  # type: ignore
from src.modules.user.ports.graphql_routers.user_router import user_gpl_router  # type: ignore

# ** info: rest based routers imports
from src.modules.centralized_analytics.ports.rest_routers.centralized_analytics_router import centralized_analytics_router  # type: ignore
from src.modules.collect_request.ports.rest_routers.collect_request_router import collect_request_router  # type: ignore
from src.modules.heart_beat.ports.rest_routers.heart_beat_router import heart_beat_router
from src.modules.parameter.ports.rest_routers.parameter_router import parameter_router
from src.modules.waste.ports.rest_routers.waster_router import waste_router
from src.modules.user.ports.rest_routers.user_router import user_router

# ** info: sidecard.middlewares imports
from src.sidecard.system.middlewares.authentication_handler_middleware import AuthenticationHandlerMiddleware  # type: ignore
from src.sidecard.system.middlewares.logger_contextualizer_middleware import LoggerContextualizerMiddleware  # type: ignore
from src.sidecard.system.middlewares.error_handler_middleware import ErrorHandlerMiddleware  # type: ignore

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
# ** info: initializing graphql based routers
# ---------------------------------------------------------------------------------------------------------------------

routes: List[Route] = []

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting graphql based routers
# ---------------------------------------------------------------------------------------------------------------------

routes.append(waste_gpl_router)
routes.append(user_gpl_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: mounting graphql based routers
# ---------------------------------------------------------------------------------------------------------------------

graphql_routers: List[BaseRoute] = [Mount(path=path_provider.build_posix_path("graphql"), routes=routes)]

# ---------------------------------------------------------------------------------------------------------------------
# ** info: initializing app metadata and documentation
# ---------------------------------------------------------------------------------------------------------------------

metadata: Dict[str, Any] = {
    "description": "This repository corresponds to the a small python microservice that is going to be used used in the sar system.",
    "summary": "Service incharge of managing wastes, collect request, and system parameters.",
    "title": "Sar Python Microservice",
    "version": "v3.2.1",
}

sar_core_soa: FastAPI
if env_provider.app_swagger_docs is True:
    sar_core_soa = FastAPI(routes=graphql_routers, docs_url=path_provider.build_posix_path("rest", "docs"), redoc_url=None, swagger_ui_parameters={"defaultModelsExpandDepth": -1}, **metadata)  # noqa # fmt: skip
    logging.warning("swagger docs active")
else:
    sar_core_soa = FastAPI(routes=graphql_routers, docs_url=None, redoc_url=None, **metadata)
    logging.warning("swagger docs inactive")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest base router
# ---------------------------------------------------------------------------------------------------------------------

rest_router: APIRouter = APIRouter(prefix=path_provider.build_posix_path("rest"))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting rest routers
# ---------------------------------------------------------------------------------------------------------------------

rest_router.include_router(router=centralized_analytics_router)
rest_router.include_router(router=collect_request_router)
rest_router.include_router(router=heart_beat_router)
rest_router.include_router(router=parameter_router)
rest_router.include_router(router=waste_router)
rest_router.include_router(router=user_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: mounting rest based routers
# ---------------------------------------------------------------------------------------------------------------------

sar_core_soa.include_router(rest_router)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: setting up app middlewares
# ---------------------------------------------------------------------------------------------------------------------

if env_provider.app_use_authentication_handler_middleware is True:
    logging.info("authentication middleware active")
    sar_core_soa.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=AuthenticationHandlerMiddleware())
else:
    logging.warning("authentication middleware inactive")

sar_core_soa.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=ErrorHandlerMiddleware())
sar_core_soa.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=LoggerContextualizerMiddleware())
sar_core_soa.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------------------------------------------------------------------------------------------------
# ** info: erasing unnecessary artifacts builded during the app setup
# ---------------------------------------------------------------------------------------------------------------------

del path_provider
gc.collect()

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
    "app": sar_core_soa if env_provider.app_environment_mode == "production" else "sar_core_soa:sar_core_soa",
    "log_level": "debug" if env_provider.app_environment_mode != "production" else "error",
    "use_colors": False if env_provider.app_environment_mode == "production" else True,
    "reload": False if env_provider.app_environment_mode == "production" else True,
    "reload_excludes": ["**/*.pyc", "**/*.pyc.*", "**/*.pyo"],
    "reload_includes": ["**/*.py", "**/*.graphql"],
    "port": env_provider.app_server_port,
    "access_log": False,
    "host": "0.0.0.0",
}

logging.info(f"logger level set to {env_provider.app_logging_level.value} mode")
logging.info(f"application starting on port {env_provider.app_server_port}")
logging.info(f"application timezone set to {env_provider.app_time_zone.value}")
logging.info(f"application locale set to {env_provider.app_posix_locale.value}")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: running app using the previous uvicorn asgi server settings
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(**uvicorn_server_configs)

if env_provider.app_environment_mode == "production":
    logging.debug("application ended")
