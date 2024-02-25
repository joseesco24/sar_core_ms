# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import List

__all__: list[str] = ["ParameterDtos"]


class ParameterDtos:

    class ParameterSearchRequestDto(BaseModel):
        domain: str = Field(...)

        model_config = {"json_schema_extra": {"examples": [{"domain": "wasteType"}]}}

    class ParameterSearchResponseDto(BaseModel):
        values: List["ParameterDtos.ParameterDataDto"] = Field(...)

        model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "values": [
                            {"label": "Radioterapia", "value": 1},
                            {"label": "Combustible Nuclear", "value": 2},
                            {"label": "RadiografÃ­a industrial", "value": 3},
                        ]
                    }
                ]
            }
        }

    class ParameterDataDto(BaseModel):
        label: str = Field(...)
        value: int = Field(...)
