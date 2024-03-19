# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging

# ** info: typing imports
from typing import Callable
from typing import Self

# ** info: loguru imports
from loguru import logger

# ** info: starlette imports
from starlette.responses import StreamingResponse
from starlette.requests import Request

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider
from src.general_sidecards.artifacts.uuid_provider import UuidProvider


__all__: list[str] = ["LoggerContextualizerMiddleware"]


class LoggerContextualizerMiddleware:

    def __init__(self: Self) -> None:
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._uuid_provider: UuidProvider = UuidProvider()

    async def __call__(
        self: Self,
        request: Request,
        call_next: Callable,
    ) -> StreamingResponse:

        external_id: str = request.headers[r"request-id"] if r"request-id" in request.headers else r"unknown"
        internal_id: str = self._uuid_provider.get_str_uuid()
        full_url: str = str(request.url)

        response: StreamingResponse

        with logger.contextualize(
            startTimestamp=self._datetime_provider.get_current_time(),
            internalId=internal_id,
            externalId=external_id,
        ):
            logging.debug("starting request")
            logging.info(f"request url: {request.method} - {full_url}")
            logging.debug("logger contextualizer middleware started")

            response = await call_next(request)

            logging.debug("logger contextualizer middleware ended")
            logging.info(f"request ended with status {response.status_code}")
            logging.debug("request ended sucessfully")

        return response
