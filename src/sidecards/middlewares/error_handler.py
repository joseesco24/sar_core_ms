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


__all__: list[str] = ["error_handler"]


class ErrorHandler:
    async def __call__(
        self: Self,
        request: Request,
        call_next: Callable,
    ) -> StreamingResponse:
        logging.debug("error handler middleware started")

        request_context: Context = contextvars.copy_context()
        logger_kwargs: Dict = dict()

        response: StreamingResponse
        internal_id: str

        for item in request_context.items():
            if item[0].name == r"loguru_context":
                logger_kwargs = item[1]
                break

        internal_id = logger_kwargs[r"internalId"]

        try:
            response = await call_next(request)
        except Exception:
            logging.exception(f"an error has occurred while processing the request {internal_id}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={r"detail": r"Internal Server Error"})

        logging.debug("error handler middleware ended")

        return response


error_handler: ErrorHandler = ErrorHandler()
