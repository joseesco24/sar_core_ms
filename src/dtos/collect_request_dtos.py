# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional
from typing import List

__all__: list[str] = ["CollectRequestControllerDtos"]


class CollectRequestControllerDtos:
    class CollectRequestCreateRequestDto(BaseModel):
        waste: List["CollectRequestControllerDtos.RequestWasteDataDto"] = Field(...)
        request: "CollectRequestControllerDtos.RequestRequestDataDto" = Field(...)

        model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "request": {"productionCenterId": 123456789, "collectDate": "12/12/2024"},
                        "waste": [
                            {
                                "type": 1,
                                "weightInKg": 18.2,
                                "volumeInL": 19.0,
                                "packaging": 1,
                                "description": "nuclear wastes",
                                "note": "this is a note",
                            },
                            {"type": 2, "weightInKg": 18.9, "volumeInL": 18.4, "packaging": 4, "description": "bone scan wastes"},
                        ],
                    }
                ]
            }
        }

    class RequestRequestDataDto(BaseModel):
        productionCenterId: int = Field(...)
        collectDate: str = Field(...)

    class RequestWasteDataDto(BaseModel):
        weightInKg: float = Field(...)
        volumeInL: float = Field(...)
        description: str = Field(...)
        packaging: int = Field(...)
        note: Optional[str] = None
        type: int = Field(...)

    class CollectRequestCreateResponseDto(BaseModel):
        waste: Optional[List["CollectRequestControllerDtos.ResponseWasteDataDto"]] = None
        request: Optional["CollectRequestControllerDtos.ResponseRequestDataDto"] = None

        model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "request": {"productionCenterId": 123456789, "collectDate": "12/12/2024", "id": "e1899fe3-2ebf-4fcd-b168-922f75a34253"},
                        "waste": [
                            {
                                "weightInKg": 18.2,
                                "volumeInL": 19.0,
                                "description": "nuclear wastes",
                                "packaging": 1,
                                "requestId": "e1899fe3-2ebf-4fcd-b168-922f75a34253",
                                "note": "this is  a note",
                                "type": 1,
                                "id": "fa1934fa-56a8-4397-80d6-28913ff2927b",
                            },
                            {
                                "weightInKg": 18.9,
                                "volumeInL": 18.4,
                                "description": "bone scan wastes",
                                "packaging": 4,
                                "requestId": "e1899fe3-2ebf-4fcd-b168-922f75a34253",
                                "note": None,
                                "type": 2,
                                "id": "ea16dbfd-44a4-4ecb-adb4-dcad64b9f23e",
                            },
                        ],
                    }
                ]
            }
        }

    class ResponseRequestDataDto(BaseModel):
        productionCenterId: Optional[int] = None
        collectDate: Optional[str] = None
        id: Optional[str] = None

    class ResponseWasteDataDto(BaseModel):
        weightInKg: Optional[float] = None
        volumeInL: Optional[float] = None
        description: Optional[str] = None
        packaging: Optional[int] = None
        requestId: Optional[str] = None
        note: Optional[str] = None
        type: Optional[int] = None
        id: Optional[str] = None
