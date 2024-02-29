# !/usr/bin/python3
# type: ignore

# ** info: python imports
from enum import Enum

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# **info: metadata for the model imports
from src.dtos.waste_dtos_metadata import waste_clasification_req_ex
from src.dtos.waste_dtos_metadata import waste_clasification_res_ex

__all__: list[str] = ["WasteDtos"]


class WasteDtos:

    class WasteClasificationRequestDto(BaseModel):
        stateWaste: "WasteDtos.stateWasteOptions" = Field(...)
        isotopesNumber: int = Field(...)
        weightInKg: int = Field(...)
        model_config = waste_clasification_req_ex

    class stateWasteOptions(str, Enum):
        gaseous: str = "gaseous"
        liquid: str = "liquid"
        paslm: str = "paslm"
        solid: str = "solid"

    class WasteClasificationResponseDto(BaseModel):
        activityType: int = Field(...)
        model_config = waste_clasification_res_ex
