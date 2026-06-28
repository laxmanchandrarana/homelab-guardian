from fastapi import APIRouter

from guardian.prediction import prediction_service
router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)

@router.get("/{service_name}")
def predict(service_name: str):
    return prediction_service.predict(service_name)
