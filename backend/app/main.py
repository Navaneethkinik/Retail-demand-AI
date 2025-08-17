from fastapi import FastAPI
from backend.app.api import forecast

app = FastAPI(title="Demand Forecasting API")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Register routers
app.include_router(forecast.router, prefix="/api/v1/forecast", tags=["Forecast"])
