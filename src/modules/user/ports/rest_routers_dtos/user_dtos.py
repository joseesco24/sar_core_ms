# !/usr/bin/python3
# type: ignore

# ** info: pydantic imports
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# **info: metadata for the model imports
from src.modules.user.ports.rest_routers_dtos.user_dtos_metadata import user_creation_req_ex
from src.modules.user.ports.rest_routers_dtos.user_dtos_metadata import user_creation_res_ex
from src.modules.user.ports.rest_routers_dtos.user_dtos_metadata import user_by_email_req_ex

__all__: list[str] = ["UserCreationRequestDto", "UserCreationResponseDto"]


# !------------------------------------------------------------------------
# ! info: sub module dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------

# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class UserCreationRequestDto(BaseModel):
    email: EmailStr = Field(..., max_length=200)
    name: str = Field(..., max_length=255)
    lastName: str = Field(..., max_length=255)

    model_config = user_creation_req_ex


class UserByEmailRequestDto(BaseModel):
    email: EmailStr = Field(..., max_length=200)

    model_config = user_by_email_req_ex


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class UserCreationResponseDto(BaseModel):
    id: str = Field(...)
    active: bool = Field(...)
    email: EmailStr = Field(...)
    name: str = Field(...)
    lastName: str = Field(...)
    create: str = Field(...)
    update: str = Field(...)

    model_config = user_creation_res_ex
