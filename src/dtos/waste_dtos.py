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
from src.dtos.waste_dtos_metadata import waste_clasification_req_ex
from src.dtos.waste_dtos_metadata import waste_clasification_res_ex

__all__: list[str] = ["WasteDtos"]


class WasteDtos:

    class WasteClasificationRequestDto(BaseModel):
        stateWaste: "WasteDtos.stateWasteOptions" = Field(...)
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

    class stateWasteOptions(str, Enum):
        gaseous: str = "gaseous"
        liquid: str = "liquid"
        paslm: str = "paslm"
        solid: str = "solid"

    class WasteClasificationResponseDto(BaseModel):
        activityType: int = Field(...)
        model_config = waste_clasification_res_ex
