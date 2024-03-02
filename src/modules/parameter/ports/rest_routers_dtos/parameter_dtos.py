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
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos_metadata import parameter_searc_req_ex
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos_metadata import parameter_searc_res_ex

__all__: list[str] = ["ParameterSearchRequestDto", "ParameterSearchResponseDto"]


# !------------------------------------------------------------------------
# ! info: sumbodule dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------


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


# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class ParameterSearchRequestDto(BaseModel):
    domain: str = Field(...)
    model_config = parameter_searc_req_ex


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class ParameterSearchResponseDto(BaseModel):
    values: List[ParameterDataDto] = Field(...)
    model_config = parameter_searc_res_ex
