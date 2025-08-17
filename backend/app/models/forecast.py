from pydantic import BaseModel
from typing import List

class ForecastRequest(BaseModel):
    history: List[float]  # e.g. past sales

class ForecastResponse(BaseModel):
    prediction: List[float]
