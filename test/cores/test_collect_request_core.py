# !/usr/bin/python3

# ** info: python imports
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateResponseDto  # type: ignore

# ** info: core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore  # type: ignore

# ** info: fixtures imports
from test_collect_request_core_fixtures import request_create_response_fixture_1  # type: ignore
from test_collect_request_core_fixtures import request_create_request_fixture_1  # type: ignore
from test_collect_request_core_fixtures import parameters_ids_fixture_1  # type: ignore
from test_collect_request_core_fixtures import collect_request  # type: ignore
from test_collect_request_core_fixtures import wastes_list  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ** info: only the methods that interact with external systems are mocked, the rest of the methods are tested
# !! info: this includes only adapters from the same module and cpms (core port methods) from other cores
# ---------------------------------------------------------------------------------------------------------------------

collect_request_core: CollectRequestCore = CollectRequestCore()
collect_request_core._parameter_core.cpm_pc_get_set_of_parameter_ids_by_domain = AsyncMock(return_value=parameters_ids_fixture_1)  # type: ignore
collect_request_core._waste_core.cpm_wc_create_waste_with_basic_info = AsyncMock(side_effect=wastes_list)  # type: ignore
collect_request_core._collect_request_provider.store_collect_request = MagicMock(return_value=collect_request)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ** info: only the drivers are explicitly tested, the rest of the methods are implicitly tested
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_create_request_hpp1() -> None:
    request_create_response: CollectRequestCreateResponseDto = await collect_request_core.driver_create_request(request_create_request=request_create_request_fixture_1)
    assert request_create_response == request_create_response_fixture_1
