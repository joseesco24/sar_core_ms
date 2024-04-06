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
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_id_note_store_id_dto_req
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_creation_req_ex
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_creation_res_ex
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_modify_state_by_id_res_dto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_find_by_status_req_dto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_find_by_status_res_dto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_modify_state_by_id_req_dto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos_metadata import collect_request_id_note_dto

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.datetime_provider import DatetimeProvider
from src.sidecard.system.artifacts.uuid_provider import UuidProvider

__all__: list[str] = ["CollectRequestFullDataResponseDto", "CollectRequestCreateRequestDto"]


# !------------------------------------------------------------------------
# ! info: sub module dtos section start
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
    id: str = Field(...)
    requestId: str = Field(...)
    type: int = Field(...)
    packaging: int = Field(...)
    processStatus: int = Field(...)
    weightInKg: float = Field(...)
    volumeInL: float = Field(...)
    isotopesNumber: Optional[float] = None
    stateWaste: Optional[int] = None
    storeType: Optional[int] = None
    description: str = Field(...)
    note: Optional[str] = None
    create: str = Field(...)
    update: str = Field(...)

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

    @field_validator("id", "requestId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value


class ResponseRequestDataDto(BaseModel):
    id: str = Field(...)
    collectDate: str = Field(...)
    processStatus: int = Field(...)
    productionCenterId: int = Field(...)
    note: Optional[str] = None
    create: str = Field(...)
    update: str = Field(...)

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

    @field_validator("id")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    model_config = collect_request_modify_state_by_id_res_dto


# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class CollectRequestCreateRequestDto(BaseModel):
    waste: List[RequestWasteDataDto] = Field(...)
    request: RequestRequestDataDto = Field(...)
    model_config = collect_request_creation_req_ex


class CollectRequestFindByStatusReqDto(BaseModel):
    processStatus: int = Field(...)

    @field_validator("processStatus")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = collect_request_find_by_status_req_dto


class CollectRequestIdNoteDto(BaseModel):
    collectReqId: str = Field(...)
    note: str = Field(...)

    @field_validator("collectReqId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    model_config = collect_request_id_note_dto


class CollectRequestIdNoteStoreIdDto(BaseModel):
    collectReqId: str = Field(...)
    note: str = Field(...)
    storeId: int = Field(...)

    @field_validator("collectReqId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    @field_validator("storeId")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = collect_request_id_note_store_id_dto_req


class CollectRequestModifyByIdReqDto(BaseModel):
    collectReqId: str = Field(...)
    processStatus: int = Field(...)
    note: str = Field(...)

    @field_validator("collectReqId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    model_config = collect_request_modify_state_by_id_req_dto


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class CollectRequestFullDataResponseDto(BaseModel):
    waste: List[ResponseWasteDataDto] = Field(...)
    request: ResponseRequestDataDto = Field(...)
    model_config = collect_request_creation_res_ex


class CollectRequestFindByStatusResDto(BaseModel):
    values: List[ResponseRequestDataDto] = Field(...)
    model_config = collect_request_find_by_status_res_dto
