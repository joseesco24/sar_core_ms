# !/usr/bin/python3

# ** info: python imports
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "."))

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore

# ** info: core imports
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: fixtures imports
from test_waste_core_fixtures import update_waste_casification_request_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_clasification_response_fixture_1  # type: ignore
from test_waste_core_fixtures import parameter_search_request_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_full_data_response_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_1  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ---------------------------------------------------------------------------------------------------------------------

waste_core: WasteCore = WasteCore()
waste_core._parameter_core.cpm_pc_get_set_of_parameter_ids_by_domain = AsyncMock(return_value=set([1]))  # type: ignore
waste_core._waste_provider.update_waste_internal_classification_info = MagicMock(return_value=waste_1)  # type: ignore
waste_core._brms_service.obtain_waste_clasification = MagicMock(return_value=1)  # type: ignore

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


@mark.asyncio
async def test_driver_update_waste_classify_classify_1() -> None:
    waste_clasification_response: WasteFullDataResponseDto = await waste_core.driver_update_waste_classify(waste_classify_request=update_waste_casification_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert waste_clasification_response == waste_full_data_response_fixture_1
