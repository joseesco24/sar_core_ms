# !/usr/bin/python3
# type: ignore

# ** info: python imports
from enum import Enum

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

# **info: metadata for the model imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import collect_request_classify_req_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import collect_request_classify_res_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_clasification_req_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_clasification_res_ex

__all__: list[str] = ["WasteClasificationRequestDto", "WasteClasificationResponseDto", "WasteClassifyRequestDto", "WasteClassifyResponseDto"]


# !------------------------------------------------------------------------
# ! info: sumbodule dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------


class StateWasteOptions(str, Enum):
    gaseous: str = "gaseous"
    liquid: str = "liquid"
    paslm: str = "paslm"
    solid: str = "solid"


# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class WasteClasificationRequestDto(BaseModel):
    stateWaste: StateWasteOptions = Field(...)
    isotopesNumber: float = Field(...)
    weightInKg: float = Field(...)
    model_config = waste_clasification_req_ex

    @field_validator("isotopesNumber", "weightInKg")
    @classmethod
    def int_validator(cls, value: float, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a double input")
        return value


class WasteClassifyRequestDto(BaseModel):
    wasteId: str = Field(...)
    isotopesNumber: float = Field(...)
    stateWaste: int = Field(...)
    storeId: int = Field(...)

    @field_validator("isotopesNumber")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("stateWaste", "storeId")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = collect_request_classify_req_ex


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class WasteClasificationResponseDto(BaseModel):
    activityType: int = Field(...)
    model_config = waste_clasification_res_ex


class WasteClassifyResponseDto(BaseModel):
    code: int = Field(...)
    message: str = Field(...)

    @field_validator("code")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = collect_request_classify_res_ex
