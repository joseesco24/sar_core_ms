# !/usr/bin/python3

# ** info: python imports
from unittest.mock import MagicMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore

# ** info: core imports
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create needed artifcts
# ---------------------------------------------------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ---------------------------------------------------------------------------------------------------------------------

waste_core: WasteCore = WasteCore()
waste_core._brms_service.obtain_waste_clasification = MagicMock(return_value=1)  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameter_search_request_fixture_1: WasteClasificationRequestDto = WasteClasificationRequestDto(
    stateWaste="liquid",  # type: ignore
    isotopesNumber=1.0,
    weightInKg=1.0,
)

waste_clasification_response_fixture_1: WasteClasificationResponseDto = WasteClasificationResponseDto(
    storeType=1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_obtain_waste_classify_1() -> None:
    waste_clasification_response: WasteClasificationResponseDto = await waste_core.driver_obtain_waste_classify(parameter_search_request=parameter_search_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert waste_clasification_response == waste_clasification_response_fixture_1
