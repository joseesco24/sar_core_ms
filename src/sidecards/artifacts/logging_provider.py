# !/usr/bin/python3
# type: ignore

# ** info: python imports
import traceback
import logging
import json
import sys

# ** info: typing imports
from typing import Union
from typing import Dict
from typing import Self
from typing import Any

# ** info: types imports
from types import TracebackType
from types import FrameType

# ** info: loguru imports
from loguru import logger

# ** info: loguru _recattrs imports
from loguru._recattrs import RecordException

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider


__all__: list[str] = ["LoggingProvider"]


class LoggingProvider:
    _extras: Dict[str, str] = {
        "internalId": "397d4343-2855-4c92-b64b-58ee82006e0b",
        "externalId": "397d4343-2855-4c92-b64b-58ee82006e0b",
        "version": "v2.3.0",
    }
    _datetime_provider: DatetimeProvider = DatetimeProvider()

    @classmethod
    def setup_pretty_logging(cls) -> None:
        """setup pretty logging
        this function overwrites the python root logger with a custom logger, so all the logs are
        written with the new overwritten configuration
        """

        fmt: str = (
            "[{extra[version]}][<fg #66a3ff>{time:YYYY-MM-DD HH:mm:ss.SSSSSS!UTC}</fg #66a3ff>:<fg #fc03cf>{extra[internalId]}</fg #fc03cf>] <level>{level}</level>: {message}"
        )

        # ** info: overwriting all the loggers configs with the new one
        logging.root.handlers = [cls._CustomInterceptHandler()]
        logging.root.setLevel(logging.DEBUG)

        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = list()
            logging.getLogger(name).propagate = True

        # ** info: loguru configs
        loguru_configs: dict = {
            "sink": sys.stdout,
            "serialize": False,
            "colorize": True,
            "format": fmt,
        }

        logger.configure(patcher=lambda record: cls._pretty_record_patcher(record), extra=cls._extras, handlers=[loguru_configs])

    @classmethod
    def setup_structured_logging(cls) -> None:
        """setup structured logging
        this function overwrites the python root logger with a custom logger, so all the logs are
        written with the new overwritten configuration
        """

        fmt: str = "{message}"

        # ** info: overwriting all the loggers configs with the new one
        logging.root.handlers = [cls._CustomInterceptHandler()]
        logging.root.setLevel(logging.DEBUG)

        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = list()
            logging.getLogger(name).propagate = True

        # ** info: loguru configs
        loguru_configs: dict = {
            "sink": cls._pretty_log_sink,
            "serialize": True,
            "colorize": False,
            "format": fmt,
        }

        logger.configure(extra=cls._extras, handlers=[loguru_configs])

    @classmethod
    def _pretty_record_patcher(cls, record: logging.LogRecord) -> logging.LogRecord:
        if record["level"].name == "INFO" or record["level"].name == "DEBUG":
            record["message"] = str(record["message"]).replace("\n", " ")
        return record

    @classmethod
    def _pretty_log_sink(cls, message: str) -> None:
        serialized = cls._custom_serializer(message.record)
        sys.stdout.write(serialized)
        sys.stdout.write("\n")
        sys.stdout.flush()

    @classmethod
    def _custom_serializer(cls, record) -> str:
        subset: Dict[str, Any] = {
            "severity": record["level"].name,
            "timestamp": cls._datetime_provider.get_utc_pretty_string(),
            "message": record["message"],
            "externalId": record["extra"]["externalId"],
            "internalId": record["extra"]["internalId"],
            "version": record["extra"]["version"],
        }

        if record["exception"] is not None:
            error: RecordException = record["exception"]

            error_traceback: TracebackType = error.traceback
            error_message: str = error.value.args[0]
            error_type: str = error.type.__name__
            string_traceback: str

            string_traceback = "".join(traceback.format_tb(error_traceback))

            subset["erro"] = {
                "type": error_type,
                "message": error_message,
                "traceback": string_traceback,
            }

        return json.dumps(subset)

    class _CustomInterceptHandler(logging.Handler):
        def emit(self: Self, record: logging.LogRecord):
            level: Union[str, int]

            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame: FrameType = logging.currentframe()
            depth: int = 2

            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
