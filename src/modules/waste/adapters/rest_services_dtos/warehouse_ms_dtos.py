# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

__all__: list[str] = ["WarehouseFullDataResponseDto"]


class WarehouseFullDataResponseDto(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    warehouse_type: str = Field(...)
    address: str = Field(...)
    latitude: str = Field(...)
    longitude: str = Field(...)
    capacity: float = Field(...)
    is_temporal: bool = Field(...)

    @field_validator("capacity")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("id")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    @field_validator("is_temporal")
    @classmethod
    def bool_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, bool):
            value = bool(value)
        else:
            raise ValueError(f"{info.field_name} is not a boolean input")
        return value


class WarehouseFullDataRequestDto(BaseModel):
    id: int = Field(...)
    nameStore: str = Field(...)
    typeStoreId: str = Field(...)
    address: str = Field(...)
    latitude: str = Field(...)
    longitude: str = Field(...)
    capacity: float = Field(...)
    temporaryStorage: bool = Field(...)

    @field_validator("capacity")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("id")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    @field_validator("temporaryStorage")
    @classmethod
    def bool_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, bool):
            value = bool(value)
        else:
            raise ValueError(f"{info.field_name} is not a boolean input")
        return value
