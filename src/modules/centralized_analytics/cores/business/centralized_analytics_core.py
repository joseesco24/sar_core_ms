# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: asyncio imports
from asyncio import gather

# ** info: typing imports
from typing import Self
from typing import List
from typing import Dict
from typing import Any

# ** info: cores imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore  # type: ignore
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: dtos imports
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos import YearDataResponseDto  # type: ignore
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos import YearDataRequestDto  # type: ignore
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos import MonthAnalyticsDto  # type: ignore

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

__all__: list[str] = ["CentralyzedAnalyticsCore"]


class CentralyzedAnalyticsCore:

    # !------------------------------------------------------------------------
    # ! info: core slots section start
    # !------------------------------------------------------------------------

    __slots__ = ["_collect_request_core", "_waste_core", "_datetime_provider"]

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: cores building
        self._collect_request_core: CollectRequestCore = CollectRequestCore()
        self._waste_core: WasteCore = WasteCore()
        # ** info: sidecards building
        self._datetime_provider: DatetimeProvider = DatetimeProvider()

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_obtain_wcr_yearly_analytics(self: Self, year_data_request: YearDataRequestDto) -> YearDataResponseDto:
        logging.info("starting driver_obtain_wcr_yearly_analytics")
        collect_request_year_data, wastes_year_data = await self._get_year_wcr_data(year=year_data_request.year)
        months_merged_info: List[Dict[str, int]] = await self._merge_wcr_data(collect_request_year_data=collect_request_year_data, wastes_year_data=wastes_year_data)
        year_data_response: YearDataResponseDto = await self._map_year_wcr_response(months_merged_info=months_merged_info)
        logging.info("starting driver_obtain_wcr_yearly_analytics")
        return year_data_response

    # !------------------------------------------------------------------------
    # ! info: core adapter methods section start
    # ! warning: all the methods in this section are the ones that are going to call methods from another core
    # ! warning: a method only can be declared in this section if it is going to call a port method from another core
    # !------------------------------------------------------------------------

    async def cam_collect_req_quantity_by_year(self: Self, year: int) -> Any:
        logging.info("starting cam_collect_req_quantity_by_year")
        collect_req_quantity_by_year = await self._collect_request_core.cpm_collect_req_quantity_by_year(year=year)
        logging.info("ending cam_collect_req_quantity_by_year")
        return collect_req_quantity_by_year

    async def cam_waste_quantity_by_year(self: Self, year: int) -> Any:
        logging.info("starting cam_waste_quantity_by_year")
        collect_req_quantity_by_year = await self._waste_core.cpm_waste_quantity_by_year(year=year)
        logging.info("ending cam_waste_quantity_by_year")
        return collect_req_quantity_by_year

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

    async def _map_year_wcr_response(self: Self, months_merged_info: List[Dict[str, int]]) -> YearDataResponseDto:
        return YearDataResponseDto(
            analytics=await self._map_year_wcr_analytics(months_merged_info=months_merged_info),
        )

    async def _map_year_wcr_analytics(self: Self, months_merged_info: List[Dict[str, int]]) -> List[MonthAnalyticsDto]:
        return [
            await self._map_month_wcr_analytics(
                collect_request_quantity=month_merged_info[r"collect_request_quantity"],
                wastes_quantity=month_merged_info[r"wastes_quantity"],
                month=int(month_merged_info[r"month"]),
            )
            for month_merged_info in months_merged_info
        ]

    async def _map_month_wcr_analytics(self: Self, collect_request_quantity: int, wastes_quantity: int, month: int) -> MonthAnalyticsDto:
        return MonthAnalyticsDto(
            monthName=self._datetime_provider.get_month_literal(month_number=month),
            collectRequestsQuantity=collect_request_quantity,
            wastesQuantity=wastes_quantity,
            monthNumber=month,
        )

    async def _get_year_wcr_data(self: Self, year: int) -> tuple[Any, Any]:
        return await gather(self.cam_collect_req_quantity_by_year(year=year), self.cam_waste_quantity_by_year(year=year))

    async def _merge_wcr_data(self: Self, collect_request_year_data: List[Dict[str, int]], wastes_year_data: List[Dict[str, int]]) -> List[Dict[str, int]]:
        merged_data: Dict[str, Dict[str, int]] = {}
        for month in range(1, 12 + 1):
            merged_data[str(month)] = {r"collect_request_quantity": 0, r"wastes_quantity": 0, r"month": month}
        for collect_request_data in collect_request_year_data:
            merged_data[str(collect_request_data[r"month"])][r"collect_request_quantity"] = collect_request_data[r"quantity"]
        for waste_data in wastes_year_data:
            merged_data[str(waste_data[r"month"])][r"wastes_quantity"] = waste_data[r"quantity"]
        merged_data_return: List[Dict[str, int]] = list(merged_data.values())
        return merged_data_return
