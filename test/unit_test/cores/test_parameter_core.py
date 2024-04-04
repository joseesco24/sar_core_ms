# !/usr/bin/python3

# ** info: python imports
from unittest.mock import MagicMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "..", "."))

# ** info: dtos imports
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchResponseDto  # type: ignore

# ** info: core imports
from src.modules.parameter.cores.business.parameter_core import ParameterCore  # type: ignore

# ** info: fixtures imports
from test_parameter_core_fixtures import parameters_search_response_dto_fixture_1  # type: ignore
from test_parameter_core_fixtures import parameter_search_request_dto_fixture_1  # type: ignore
from test_parameter_core_fixtures import parameter_list_fixture_1  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ** info: only the methods that interact with external systems are mocked, the rest of the methods are tested
# !! info: this includes only adapters from the same module and cpms (core port methods) from other cores
# ---------------------------------------------------------------------------------------------------------------------

parameter_core: ParameterCore = ParameterCore()
parameter_core._parameter_provider.search_parameters_by_domain = MagicMock(return_value=parameter_list_fixture_1)  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ** info: only the drivers are explicitly tested, the rest of the methods are implicitly tested
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_search_parameter_hpp1() -> None:
    parameter_search_response: ParameterSearchResponseDto = await parameter_core.driver_search_parameter(parameter_search_request=parameter_search_request_dto_fixture_1)
    parameter_core._parameter_provider.search_parameters_by_domain.assert_called_with(domain=parameter_search_request_dto_fixture_1.domain)
    assert parameter_search_response == parameters_search_response_dto_fixture_1
