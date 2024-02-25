# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional
from typing import List

# **info: metadata for the model imports
from src.dtos.collect_request_dtos_metadata import collect_request_creation_req_ex
from src.dtos.collect_request_dtos_metadata import collect_request_creation_res_ex

__all__: list[str] = ["CollectRequestControllerDtos"]


class CollectRequestControllerDtos:
    class CollectRequestCreateRequestDto(BaseModel):
        waste: List["CollectRequestControllerDtos.RequestWasteDataDto"] = Field(...)
        request: "CollectRequestControllerDtos.RequestRequestDataDto" = Field(...)
        model_config = collect_request_creation_req_ex

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
        waste: List["CollectRequestControllerDtos.ResponseWasteDataDto"] = Field(...)
        request: "CollectRequestControllerDtos.ResponseRequestDataDto" = Field(...)
        model_config = collect_request_creation_res_ex

    class ResponseRequestDataDto(BaseModel):
        productionCenterId: int = Field(...)
        collectDate: str = Field(...)
        id: str = Field(...)

    class ResponseWasteDataDto(BaseModel):
        weightInKg: float = Field(...)
        volumeInL: float = Field(...)
        description: str = Field(...)
        packaging: int = Field(...)
        requestId: str = Field(...)
        note: Optional[str] = None
        type: int = Field(...)
        id: str = Field(...)
