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

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: artifacts imports
from src.sidecards.env.configs import configs


__all__: list[str] = ["BrmsPort"]


class BrmsPort:
    def __init__(self: Self):
        self.base_url: str = str(configs.sar_brms_base_url)

    def obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        data: dict[str, str] = {"stateWaste": state_waste, "weightInKg": weight_in_kg, "isotopesNumber": isotopes_number}
        url: str = urljoin(self.base_url, r"/brms/waste/clasification")
        raw_response: Response = httpx.post(url, json=data)

        logging.debug(f"brms url: {url}")

        if raw_response.status_code != status.HTTP_200_OK:
            logging.error("error while trying to connect to brms")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

        response: int

        try:
            response = int(raw_response.text)
        except Exception:
            logging.error("error parsing response from brms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if response == 0:
            logging.error("the waste was not classified by brms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
