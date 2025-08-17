from fastapi import APIRouter
from backend.app.models.forecast import ForecastRequest, ForecastResponse
from backend.app.services.forecast_service import generate_forecast

router = APIRouter()

@router.post("/", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    prediction = generate_forecast(req)
    return ForecastResponse(prediction=prediction)