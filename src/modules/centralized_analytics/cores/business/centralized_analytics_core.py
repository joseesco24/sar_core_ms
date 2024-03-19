# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: asyncio imports
# from asyncio import gather

# ** info: typing imports
from typing import Self
from typing import List
from typing import Dict

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
        months_merged_info: List[Dict] = [{"collect_request_quantity": 12, "wastes_quantity": 18, "month": 2}, {"collect_request_quantity": 1, "wastes_quantity": 1, "month": 1}]
        year_data_response: YearDataResponseDto = await self._map_year_wcr_response(months_merged_info=months_merged_info)
        logging.info("starting driver_obtain_wcr_yearly_analytics")
        return year_data_response

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
