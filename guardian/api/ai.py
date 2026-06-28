from fastapi import APIRouter

from guardian.ai.service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

service = AIService()


@router.get("/analyze/{service_name}")
def analyze(service_name: str):
    return service.analyze(service_name)
