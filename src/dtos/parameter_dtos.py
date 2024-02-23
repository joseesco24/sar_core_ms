# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional
from typing import List

__all__: list[str] = [
    "ParameterSearchResponseDto",
    "ParameterSearchRequestDto",
    "ParameterDataDto",
]


class ParameterSearchRequestDto(BaseModel):
    domain: str = Field(...)


class ParameterDataDto(BaseModel):
    label: Optional[str] = None
    value: Optional[int] = None


class ParameterSearchResponseDto(BaseModel):
    values: Optional[List[ParameterDataDto]] = None
