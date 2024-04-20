# !/usr/bin/python3

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserCreationResponseDto  # type: ignore
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserCreationRequestDto  # type: ignore
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserByEmailRequestDto  # type: ignore

# ** info: app core imports
from src.modules.user.core.business.user_core import UserCore  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.path_provider import PathProvider  # type: ignore

__all__: list[str] = ["user_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
user_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("user"), tags=["Users"])

# ** info: building router core
_user_core: UserCore = UserCore()


@user_router.post(
    description="allow to create a new user",
    summary="allow to create a new user",
    path=_path_provider.build_posix_path("create"),
    response_model=UserCreationResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_create_user(user_creation_request: UserCreationRequestDto = Body(...)) -> UserCreationResponseDto:
    user_creation_response: UserCreationResponseDto = await _user_core.driver_create_user(user_creation_request)
    return user_creation_response


@user_router.post(
    description="allow to get a user info by its email",
    summary="allow to get a user info by its email",
    path=_path_provider.build_posix_path("search-by-email"),
    response_model=UserCreationResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_by_email(user_by_email_request: UserByEmailRequestDto = Body(...)) -> UserCreationResponseDto:
    user_by_email_response: UserCreationResponseDto = await _user_core.driver_get_user_by_email(user_by_email_request)
    return user_by_email_response
