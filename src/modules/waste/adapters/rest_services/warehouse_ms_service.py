# !/usr/bin/python3
# type: ignore

# ** info: python imports
from urllib.parse import urljoin
import logging

# ** info: typing imports
from typing import Self

# ** info: httpx imports
from httpx import Response
import httpx

# ** info: stamina imports
from stamina import retry

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: dtos imports
from src.modules.waste.adapters.rest_services_dtos.warehouse_ms_dtos import WarehouseFullDataResponseDto
from src.modules.waste.adapters.rest_services_dtos.warehouse_ms_dtos import WarehouseFullDataRequestDto

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache

# ** info: asyncache imports
from asyncache import cached as async_cached

__all__: list[str] = ["WarehouseMsService"]

# ** info: creating a shared cache for all the warehouse ms service instances
warehouse_ms_service_cache: TTLCache = TTLCache(ttl=10, maxsize=20)


class WarehouseMsService:
    def __init__(self: Self):
        self._env_provider: EnvProvider = EnvProvider()
        self.base_url: str = str(self._env_provider.sar_warehouse_ms_base_url)
        self._httpx_client: httpx.AsyncClient = httpx.AsyncClient()

    def clear_cache(self: Self) -> None:
        warehouse_ms_service_cache.clear()

    @async_cached(warehouse_ms_service_cache)
    @retry(on=HTTPException, attempts=8, wait_initial=0.4, wait_exp_base=2)
    async def obtain_warehouse_full_data(self: Self, warehouse_id: int) -> WarehouseFullDataResponseDto:
        logging.debug("obtaining warehouse full data from warehouse ms")
        url: str = urljoin(self.base_url, f"/store/{warehouse_id}")
        warehouse_full_data: WarehouseFullDataResponseDto
        logging.debug(f"warehouse ms url: {url}")
        try:
            raw_response: Response = await self._httpx_client.get(url=url, timeout=10)
        except Exception:
            logging.error("error unable to connect to warehouse ms")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if raw_response.status_code != status.HTTP_200_OK:
            logging.error("the warehouse ms didnt respond correctly")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            warehouse_full_data = await self._map_warehouse_ms_dict_to_full_data_dto(warehouse_full_data_dict=raw_response.json())
        except Exception:
            logging.error("error parsing response from warehouse ms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logging.debug("warehouse full data obtained from warehouse ms")
        return warehouse_full_data

    @retry(on=HTTPException, attempts=8, wait_initial=0.4, wait_exp_base=2)
    async def update_warehouse_full_data(self: Self, warehouse_id: int, warehouse_current_full_data: WarehouseFullDataResponseDto) -> WarehouseFullDataResponseDto:
        logging.debug("updating warehouse full data on warehouse ms")
        url: str = urljoin(self.base_url, f"/store/{warehouse_id}")
        warehouse_full_data: WarehouseFullDataResponseDto
        logging.debug(f"warehouse ms url: {url}")
        try:
            data: WarehouseFullDataRequestDto = await self._map_warehouse_full_data_dto_to_ms_dict(warehouse_full_data=warehouse_current_full_data)
            raw_data: dict[str, any] = data.model_dump()
        except Exception:
            logging.error("error parsing request for warehouse ms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            raw_response: Response = await self._httpx_client.put(url=url, json=raw_data, timeout=10)
        except Exception:
            logging.error("error unable to connect to warehouse ms")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if raw_response.status_code != status.HTTP_200_OK:
            logging.error("the warehouse ms didnt respond correctly")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            warehouse_full_data = await self._map_warehouse_ms_dict_to_full_data_dto(warehouse_full_data_dict=raw_response.json())
        except Exception:
            logging.error("error parsing response from warehouse ms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.clear_cache()
        logging.debug("warehouse full data updated on warehouse ms")
        return warehouse_full_data

    async def obtain_warehouse_current_capacity(self: Self, warehouse_id: int) -> float:
        logging.debug("obtaining warehouse current capacity from warehouse ms")
        warehouse_full_data: WarehouseFullDataResponseDto = await self.obtain_warehouse_full_data(warehouse_id=warehouse_id)
        logging.debug("warehouse current capacity obtained from warehouse ms")
        return warehouse_full_data.capacity

    async def update_warehouse_current_capacity(self: Self, warehouse_id: int, new_warehouse_capacity: float) -> float:
        logging.debug("updating warehouse current capacity on warehouse ms")
        warehouse_full_data: WarehouseFullDataResponseDto = await self.obtain_warehouse_full_data(warehouse_id=warehouse_id)
        warehouse_full_data.capacity = new_warehouse_capacity
        update_warehouse_data: WarehouseFullDataResponseDto = await self.update_warehouse_full_data(warehouse_id=warehouse_id, warehouse_current_full_data=warehouse_full_data)
        logging.debug("warehouse current capacity updated on warehouse ms")
        return update_warehouse_data.capacity

    async def _map_warehouse_ms_dict_to_full_data_dto(self: Self, warehouse_full_data_dict: dict[str, any]) -> WarehouseFullDataResponseDto:
        return WarehouseFullDataResponseDto(
            is_temporal=warehouse_full_data_dict["temporaryStorage"],
            warehouse_type=warehouse_full_data_dict["typeStoreId"],
            longitude=warehouse_full_data_dict["longitude"],
            latitude=warehouse_full_data_dict["latitude"],
            capacity=warehouse_full_data_dict["capacity"],
            address=warehouse_full_data_dict["address"],
            name=warehouse_full_data_dict["nameStore"],
            id=warehouse_full_data_dict["id"],
        )

    async def _map_warehouse_full_data_dto_to_ms_dict(self: Self, warehouse_full_data: WarehouseFullDataResponseDto) -> dict[str, any]:
        return WarehouseFullDataRequestDto(
            temporaryStorage=warehouse_full_data.is_temporal,
            typeStoreId=warehouse_full_data.warehouse_type,
            longitude=warehouse_full_data.longitude,
            latitude=warehouse_full_data.latitude,
            capacity=warehouse_full_data.capacity,
            address=warehouse_full_data.address,
            nameStore=warehouse_full_data.name,
            id=warehouse_full_data.id,
        )
