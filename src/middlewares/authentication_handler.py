# !/usr/bin/python3
# type: ignore

# ** info: python imports
from contextvars import Context
from typing import Callable
import contextvars
import logging

# ** info: typing imports
from typing import Self
from typing import Dict

# ** info: starlette imports
from starlette.responses import StreamingResponse
from starlette.requests import Request

# ** info: fastapi imports
from fastapi.responses import JSONResponse
from fastapi import status


from src.artifacts.env.configs import configs

__all__: list[str] = ["authentication_handler"]


class AuthenticationHandler:
    async def __call__(
        self: Self,
        request: Request,
        call_next: Callable,
    ) -> StreamingResponse:
        logging.debug("authentication middleware started")

        endpoint_url: str = request.url.replace(request.base_url, "").strip().lower()
        request_context: Context = contextvars.copy_context()
        is_authenticated: bool = False
        logger_kwargs: Dict = dict()

        response: StreamingResponse
        internal_id: str

        for item in request_context.items():
            if item[0].name == r"loguru_context":
                logger_kwargs = item[1]
                break

        internal_id = logger_kwargs[r"internalId"]

        if endpoint_url in configs.app_authentication_handler_middleware_exclude:
            logging.info("jumping authentication middleware validations")
            is_authenticated = True
        else:
            # todo: create a real authentication logic here
            is_authenticated = True

        if is_authenticated:
            logging.info(f"the request with id {internal_id} was successfully authorized")
            response: StreamingResponse = await call_next(request)
        else:
            logging.error(f"the request with id {internal_id} was not successfully authorized")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={r"detail": r"Internal Server Error"})

        logging.debug("authentication middleware ended")

        return response


authentication_handler: AuthenticationHandler = AuthenticationHandler()
