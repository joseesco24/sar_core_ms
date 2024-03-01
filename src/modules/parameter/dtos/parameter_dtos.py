# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import List

# **info: metadata for the model imports
from src.modules.parameter.dtos.parameter_dtos_metadata import parameter_searc_req_ex
from src.modules.parameter.dtos.parameter_dtos_metadata import parameter_searc_res_ex

__all__: list[str] = ["ParameterDtos"]


class ParameterDtos:

    class ParameterSearchRequestDto(BaseModel):
        domain: str = Field(...)
        model_config = parameter_searc_req_ex

    class ParameterSearchResponseDto(BaseModel):
        values: List["ParameterDtos.ParameterDataDto"] = Field(...)
        model_config = parameter_searc_res_ex

    class ParameterDataDto(BaseModel):
        label: str = Field(...)
        value: int = Field(...)

        @field_validator("value")
        @classmethod
        def int_validator(cls, value: int, info: ValidationInfo) -> int:
            if isinstance(value, int):
                value = int(value)
            else:
                raise ValueError(f"{info.field_name} is not a integer input")
            return value
