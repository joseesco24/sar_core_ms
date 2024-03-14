# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import Dict

# ** info: sidecards.constants imports
from src.business_sidecards.constants.collect_request_states_constants import CollectRequestStates  # type: ignore
from src.business_sidecards.constants.waste_states_constants import WasteStates  # type: ignore


__all__: list[str] = ["BusinessGlossaryTranslateProvider"]


class BusinessGlossaryTranslateProvider:

    def __init__(self: Self) -> None:
        self.dict_waste_status_by_collect_request_status: Dict[str, int] = {
            str(CollectRequestStates.finished): WasteStates.waste_clasification_in_course,
            str(CollectRequestStates.approved): WasteStates.collect_in_course,
            str(CollectRequestStates.rejected): WasteStates.collect_rejected,
            str(CollectRequestStates.in_review): WasteStates.in_review,
        }

    async def select_waste_status_by_collect_request_status(self: Self, collect_request_status: int) -> int:
        return self.dict_waste_status_by_collect_request_status.get(str(collect_request_status))
