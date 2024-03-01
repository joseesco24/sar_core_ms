# !/usr/bin/python3
# type: ignore

# ** info: python imports
import uuid

# ** info: typing imports
from typing import Self


__all__: list[str] = ["uuid_provider"]


class UuidProvider:
    def get_str_uuid(self: Self) -> str:
        return str(uuid.uuid4())


uuid_provider: UuidProvider = UuidProvider()
