# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging

# ** info: typing imports
from typing import Callable
from typing import Dict
from typing import Self
from typing import Any

# ** info: loguru imports
from loguru import logger

# ** info: starlette imports
from starlette.responses import StreamingResponse
from starlette.datastructures import Headers
from starlette.requests import Request

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider


__all__: list[str] = ["logger_contextualizer"]


class LoggerContextualizer:

    """logger contextualizer
    this class provides a custom loguru contextualizer middleware for fastapi based applications
    """

    def __init__(self: Self):
        pass

    async def __set_body__(self: Self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def __call__(
        self: Self,
        request: Request,
        call_next: Callable,
    ) -> StreamingResponse:
        await self.__set_body__(request=request)

        full_url: str = str(request.url)

        request_headers: Headers = request.headers
        headers_rep: Dict[str, Any] = dict()
        for key in request_headers.keys():
            headers_rep[key] = str(request_headers[key])

        internal_id: str = uuid_provider.get_str_uuid()

        if r"request-id" in headers_rep:
            external_id: str = headers_rep[r"request-id"]
        else:
            external_id: str = internal_id

        with logger.contextualize(
            internalId=internal_id,
            externalId=external_id,
        ):
            logging.debug("starting request")
            logging.info(f"request url: {request.method} - {full_url}")
            logging.debug("logger contextualizer middleware started")

            response: StreamingResponse = await call_next(request)
            response_status: int = response.status_code

            logging.debug("logger contextualizer middleware ended")
            logging.info(f"request ended with status {response_status}")
            logging.debug("request ended sucessfully")

        return response


logger_contextualizer: LoggerContextualizer = LoggerContextualizer()
