# !/usr/bin/python3

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import Response
from fastapi import status

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.path_provider import PathProvider  # type: ignore

__all__: list[str] = ["heart_beat_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
heart_beat_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("heart-beat"), tags=["Hart Beat"])


@heart_beat_router.post(
    description="allows to check if the service is or not healthy",
    summary="allows to check if the service is or not healthy",
    path=_path_provider.build_posix_path(""),
    status_code=status.HTTP_200_OK,
)
async def api_heart_beat() -> Response:
    return Response(status_code=status.HTTP_200_OK)
