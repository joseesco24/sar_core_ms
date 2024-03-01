# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

# **info: metadata for the model imports
from src.dtos.waste_dtos_metadata import collect_request_classify_req_ex
from src.dtos.waste_dtos_metadata import collect_request_classify_res_ex

__all__: list[str] = ["WasteRequestControllerDtos"]


class WasteRequestControllerDtos:
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


# ** info: editar esto al trabajar la tajada de los residuos
