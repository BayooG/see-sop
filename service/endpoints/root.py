from fastapi import APIRouter, Response

router = APIRouter()


@router.get(
    "/status",
    tags=["root"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    return Response("Service is up and running!")
