# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: dtos imports
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserCreationResponseDto  # type: ignore
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserCreationRequestDto  # type: ignore
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserByEmailRequestDto  # type: ignore

# ** info: entities imports
from src.modules.user.adapters.database_providers_entities.user_entity import User  # type: ignore

# ** info: providers imports
from src.modules.user.adapters.database_providers.user_provider import UserProvider  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.datetime_provider import DatetimeProvider  # type: ignore
from src.sidecard.system.artifacts.i8n_provider import I8nProvider  # type: ignore

__all__: list[str] = ["UserCore"]


class UserCore:
    # !------------------------------------------------------------------------
    # ! info: core slots section start
    # !------------------------------------------------------------------------

    __slots__ = ["_datetime_provider", "_user_provider", "_i8n"]

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: providers building
        self._user_provider: UserProvider = UserProvider()
        # ** info: sidecards building
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._i8n: I8nProvider = I8nProvider(module="user")

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_create_user(self: Self, user_creation_request: UserCreationRequestDto) -> UserCreationResponseDto:
        logging.info("starting driver_create_user")
        await self._check_if_user_exists_by_email(email=user_creation_request.email)
        new_user_data: User = await self._create_user_with_basic_info(user_creation_request=user_creation_request)
        user_creation_response: UserCreationResponseDto = await self._map_user_to_user_creation_response_dto(user=new_user_data)
        logging.info("starting driver_create_user")
        return user_creation_response

    async def driver_get_user_by_email(self: Self, user_by_email_request: UserByEmailRequestDto) -> UserCreationResponseDto:
        logging.info("starting driver_get_user_by_email")
        user_data: User = await self._search_user_by_email(email=user_by_email_request.email)
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self._i8n.message(message_key="EM002", email=user_by_email_request.email))
        user_creation_response: UserCreationResponseDto = await self._map_user_to_user_creation_response_dto(user=user_data)
        logging.info("starting driver_get_user_by_email")
        return user_creation_response

    # !------------------------------------------------------------------------
    # ! info: core adapter methods section start
    # ! warning: all the methods in this section are the ones that are going to call methods from another core
    # ! warning: a method only can be declared in this section if it is going to call a port method from another core
    # !------------------------------------------------------------------------

    # !------------------------------------------------------------------------
    # ! info: core port methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from another core
    # ! warning: a method only can be declared in this section if it is going to be called from another core
    # !------------------------------------------------------------------------

    # !------------------------------------------------------------------------
    # ! info: private class methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from inside this core
    # ! warning: a method only can be declared in this section if it is going to be called from inside this core
    # !------------------------------------------------------------------------

    async def _map_user_to_user_creation_response_dto(self: Self, user: User) -> UserCreationResponseDto:
        user_creation_response: UserCreationResponseDto = UserCreationResponseDto(
            create=self._datetime_provider.prettify_date_time_obj(date_time_obj=user.create),
            update=self._datetime_provider.prettify_date_time_obj(date_time_obj=user.update),
            id=user.uuid,
            active=user.active,
            email=user.email,
            name=user.name,
            lastName=user.last_name,
        )
        return user_creation_response

    async def _create_user_with_basic_info(self: Self, user_creation_request: UserCreationRequestDto) -> User:
        user: User = self._user_provider.create_user_with_basic_info(email=user_creation_request.email, name=user_creation_request.name, last_name=user_creation_request.lastName)
        return user

    async def _search_user_by_email(self: Self, email: str) -> User:
        user: User = self._user_provider.search_user_by_email(email=email)
        return user

    async def _check_if_user_exists_by_email(self: Self, email: str) -> None:
        user: User = self._user_provider.search_user_by_email(email=email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self._i8n.message(message_key="EM001", email=email))
