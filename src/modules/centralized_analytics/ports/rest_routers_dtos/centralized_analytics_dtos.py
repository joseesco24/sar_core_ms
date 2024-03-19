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
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos_metadata import year_data_res_dto_ex
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos_metadata import year_data_req_dto_ex

__all__: list[str] = ["YearDataRequestDto", "YearDataResponseDto"]


# !------------------------------------------------------------------------
# ! info: sumbodule dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------


class MonthAnalyticsDto(BaseModel):
    collectRequestsQuantity: int = Field(...)
    wastesQuantity: int = Field(...)
    monthNumber: int = Field(...)
    monthName: str = Field(...)

    @field_validator("collectRequestsQuantity", "wastesQuantity", "monthNumber")
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


class YearDataRequestDto(BaseModel):
    year: int = Field(...)

    @field_validator("year")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = year_data_req_dto_ex


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class YearDataResponseDto(BaseModel):
    analytics: List[MonthAnalyticsDto] = Field(...)
    model_config = year_data_res_dto_ex
