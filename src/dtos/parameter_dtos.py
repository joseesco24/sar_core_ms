# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import List

# **info: metadata for the model imports
from src.dtos.parameter_dtos_metadata import parameter_searc_req_ex
from src.dtos.parameter_dtos_metadata import parameter_searc_res_ex

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
