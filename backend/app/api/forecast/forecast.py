from fastapi import APIRouter, HTTPException, Query
import os
import pandas as pd
from ml.preprocessing import preprocess_csv
from ml.forecast import forecast_company

router = APIRouter(prefix="/v1/forecast")

DATA_STORAGE_PATH = "./data"

@router.get("/generate-forecast")
async def generate_forecast_api(
    company_name: str = Query(..., description="Registered company name"),
    forecast_horizon: int = Query(30, description="Days to forecast")
):
    """
    Generate sales forecasts for all SKUs of a company.
    """
    company_path = os.path.join(DATA_STORAGE_PATH, company_name)
    if not os.path.exists(company_path):
        raise HTTPException(status_code=404, detail="Company not found")

    # Find the latest CSV file in the company folder
    csv_files = [f for f in os.listdir(company_path) if f.endswith('.csv')]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No data file found for this company")
    latest_csv = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(company_path, f)))
    csv_path = os.path.join(company_path, latest_csv)

    try:
        df = preprocess_csv(csv_path)
        forecasts = forecast_company(df, forecast_horizon=forecast_horizon)
        # Convert DataFrames to dict for JSON response
        forecasts_json = {sku: fc.to_dict(orient="records") for sku, fc in forecasts.items()}
        return {"company": company_name, "forecasts": forecasts_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {str(e)}")