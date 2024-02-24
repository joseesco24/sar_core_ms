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
from starlette.responses import ContentStream
from starlette.requests import Request

# ** info: fastapi imports
from fastapi import status


__all__: list[str] = ["error_handler"]


class ErrorHandler:

    """error handler
    this class provides a custom error handler middleware for fastapi based applications
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
        logging.debug("error handler middleware started")

        request_context: Context = contextvars.copy_context()
        logger_kwargs: Dict = dict()

        for item in request_context.items():
            if item[0].name == r"loguru_context":
                logger_kwargs = item[1]
                break

        internal_id: str = logger_kwargs[r"internalId"]

        try:
            response: StreamingResponse = await call_next(request)

        except Exception:
            logging.exception(f"an error has occurred while processing the request {internal_id}")

            response_stream: ContentStream = iter([r"Internal Server Error"])

            response: StreamingResponse = StreamingResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=response_stream,
            )

        logging.debug("error handler middleware ended")

        return response


error_handler: ErrorHandler = ErrorHandler()
