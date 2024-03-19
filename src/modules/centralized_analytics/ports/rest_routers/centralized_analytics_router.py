# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos import YearDataResponseDto
from src.modules.centralized_analytics.ports.rest_routers_dtos.centralized_analytics_dtos import YearDataRequestDto

# ** info: app core imports
from src.modules.centralized_analytics.cores.business.centralized_analytics_core import CentralyzedAnalyticsCore

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["centralized_analytics_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
centralized_analytics_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("centralized-analytics"), tags=["Centralized Analytics"])

# ** info: building router core
_centralyzed_analytics_core: CentralyzedAnalyticsCore = CentralyzedAnalyticsCore()


@centralized_analytics_router.post(
    description="allows to obtain the wastes and collect requests quantities created in a month",
    summary="allows to obtain the wastes and collect requests quantities created in a month",
    path=_path_provider.build_posix_path("wcr", "yearly"),
    response_model=YearDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_obtain_wcr_yearly_analytics(year_data_request: YearDataRequestDto = Body(...)) -> YearDataResponseDto:
    year_data_response: YearDataRequestDto = await _centralyzed_analytics_core.driver_obtain_wcr_yearly_analytics(year_data_request)
    return year_data_response
