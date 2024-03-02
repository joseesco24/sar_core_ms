# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional
from typing import List

# **info: metadata for the model imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_creation_req_ex
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_creation_res_ex

# ** info: artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider

__all__: list[str] = ["CollectRequestCreateResponseDto", "CollectRequestCreateRequestDto"]


# !------------------------------------------------------------------------
# ! info: sumbodule dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()


class RequestWasteDataDto(BaseModel):
    weightInKg: float = Field(...)
    volumeInL: float = Field(...)
    description: str = Field(...)
    packaging: int = Field(...)
    note: Optional[str] = None
    type: int = Field(...)

    @field_validator("weightInKg", "volumeInL")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("packaging", "type")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value


class RequestRequestDataDto(BaseModel):
    productionCenterId: int = Field(...)
    collectDate: str = Field(...)

    @field_validator("productionCenterId")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    @field_validator("collectDate")
    @classmethod
    def date_validator(cls, value: int, info: ValidationInfo) -> int:
        try:
            value = datetime_provider.pretty_date_string_to_date(value)
        except ValueError:
            raise ValueError(f"{info.field_name} is not a valid dd/mm/yyyy date")
        return value


class ResponseWasteDataDto(BaseModel):
    weightInKg: float = Field(...)
    volumeInL: float = Field(...)
    description: str = Field(...)
    packaging: int = Field(...)
    requestId: str = Field(...)
    note: Optional[str] = None
    type: int = Field(...)
    id: str = Field(...)

    @field_validator("weightInKg", "volumeInL")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("packaging", "type")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value


class ResponseRequestDataDto(BaseModel):
    productionCenterId: int = Field(...)
    collectDate: str = Field(...)
    id: str = Field(...)

    @field_validator("productionCenterId")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    @field_validator("collectDate")
    @classmethod
    def date_validator(cls, value: int, info: ValidationInfo) -> int:
        try:
            datetime_provider.pretty_date_string_to_date(value)
        except ValueError:
            raise ValueError(f"{info.field_name} is not a valid dd/mm/yyyy date")
        return value


# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class CollectRequestCreateRequestDto(BaseModel):
    waste: List[RequestWasteDataDto] = Field(...)
    request: RequestRequestDataDto = Field(...)
    model_config = collect_request_creation_req_ex


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class CollectRequestCreateResponseDto(BaseModel):
    waste: List[ResponseWasteDataDto] = Field(...)
    request: ResponseRequestDataDto = Field(...)
    model_config = collect_request_creation_res_ex
