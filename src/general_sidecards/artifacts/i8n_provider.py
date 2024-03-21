# !/usr/bin/python3
# type: ignore

# ** info: python imports
from os.path import realpath
from os.path import dirname
from os.path import join
import locale
import json

# ** info: typing imports
from typing import Dict
from typing import Self

__all__: list[str] = ["I8nProvider"]


class I8nProvider:

    __slots__ = ["_locale_dir", "_messages_dict", "_logs_dict"]

    def __init__(self: Self) -> None:
        self._locale_dir: str = join(dirname(realpath(__file__)), "..", "i8n_files", locale.getlocale()[0])

        self._messages_dict: dict[str, str] = json.load(open(join(self._locale_dir, "messages.json")))

    def message(self: Self, message_key: str) -> str:
        return self._get_message_from_dict(dict=self._messages_dict, key=message_key)

    def _get_message_from_dict(self: Self, dict: Dict, key: str) -> str:
        nested_dict: str = dict[key] if key in dict else key
        return_message: str = nested_dict["message"] if "message" in nested_dict else key
        return return_message.lower()
