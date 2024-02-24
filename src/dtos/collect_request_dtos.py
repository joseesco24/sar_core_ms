# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional
from typing import List

__all__: list[str] = ["CollectRequestCreateRequestDto", "CollectRequestCreateResponseDto", "RequestRequestDataDto", "RequestWasteDataDto"]


class RequestWasteDataDto(BaseModel):
    weightInKg: float = Field(...)
    volumeInL: float = Field(...)
    description: str = Field(...)
    packaging: int = Field(...)
    note: Optional[str] = None
    type: int = Field(...)


class RequestRequestDataDto(BaseModel):
    productionCenterId: int = Field(...)
    collectDate: str = Field(...)


class CollectRequestCreateRequestDto(BaseModel):
    waste: List[RequestWasteDataDto] = Field(...)
    request: RequestRequestDataDto = Field(...)


class ResponseWasteDataDto(BaseModel):
    weightInKg: Optional[float] = None
    volumeInL: Optional[float] = None
    description: Optional[str] = None
    packaging: Optional[int] = None
    requestId: Optional[str] = None
    note: Optional[str] = None
    type: Optional[int] = None
    id: Optional[str] = None


class ResponseRequestDataDto(BaseModel):
    productionCenterId: Optional[int] = None
    collectDate: Optional[str] = None
    id: Optional[str] = None


class CollectRequestCreateResponseDto(BaseModel):
    waste: Optional[List[ResponseWasteDataDto]] = None
    request: Optional[ResponseRequestDataDto] = None
