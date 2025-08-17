from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import pandas as pd
from typing import Dict
import os

router = APIRouter()

DATA_DIR = "data"

@router.post("/upload-csv/")
async def upload_csv(
    company_name: str = Form(...),
    file: UploadFile = File(...)
) -> Dict[str, str]:
    company_folder = os.path.join(DATA_DIR, company_name)
    if not os.path.isdir(company_folder):
        raise HTTPException(status_code=404, detail="Company folder not found.")
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        save_path = os.path.join(company_folder, file.filename)
        df.to_csv(save_path, index=False)
        return {"filename": file.filename, "rows": str(len(df)), "saved_to": save_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")