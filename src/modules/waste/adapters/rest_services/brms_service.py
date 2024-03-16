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

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache

# ** info: asyncache imports
from asyncache import cached as async_cached

__all__: list[str] = ["BrmsService"]

# ** info: creating a shared cache for all the brms service instances
brms_service_cache: TTLCache = TTLCache(ttl=60, maxsize=20)


class BrmsService:
    def __init__(self: Self):
        self._env_provider: EnvProvider = EnvProvider()
        self.base_url: str = str(self._env_provider.sar_brms_base_url)
        self._httpx_client: httpx.AsyncClient = httpx.AsyncClient()

    def clear_cache(self: Self) -> None:
        brms_service_cache.clear()

    @async_cached(brms_service_cache)
    @retry(on=HTTPException, attempts=4, wait_initial=0.4, wait_exp_base=2)
    async def obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        logging.debug("obtaining waste classification from brms")
        data: dict[str, any] = {"stateWaste": state_waste, "weightInKg": weight_in_kg, "isotopesNumber": isotopes_number}
        url: str = urljoin(self.base_url, r"/brms/waste/clasification")
        response: int
        logging.debug(f"brms url: {url}")
        try:
            raw_response: Response = await self._httpx_client.post(url=url, json=data, timeout=10)
        except Exception:
            logging.critical("error unable to connect to brms")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if raw_response.status_code != status.HTTP_200_OK:
            logging.critical("the brms service didnt respond correctly")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            response = int(raw_response.text)
        except Exception:
            logging.critical("error parsing response from brms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if response == 0:
            logging.critical("the waste was not classified by the brms")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="waste not classifiable")
        logging.debug("waste classification obtained from brms")
        return response
