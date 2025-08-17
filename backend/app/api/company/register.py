# from dotenv import load_dotenv
import os
import shutil
from io import StringIO
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse

# Load env vars
# load_dotenv()
# DATA_STORAGE_PATH = os.getenv("DATA_STORAGE_PATH", "./data")

DATA_STORAGE_PATH = "./data"


router = APIRouter(prefix="/v1/company")  # Added prefix here

@router.post("/register-company")
async def register_company(company_name: str = Form(...)):
    """
    Registers a new company and creates its data folder.
    """
    company_path = os.path.join(DATA_STORAGE_PATH, company_name)
    
    if os.path.exists(company_path):
        raise HTTPException(status_code=400, detail="Company already registered")
    
    os.makedirs(company_path, exist_ok=True)
    return {"status": "success", "company": company_name, "path": company_path}

@router.delete("/delete-company")
async def delete_company(company_name: str = Form(...)):
    """
    Deletes a company and its data folder.
    """
    company_path = os.path.join(DATA_STORAGE_PATH, company_name)
    
    if not os.path.exists(company_path):
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        shutil.rmtree(company_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete company: {str(e)}")
    
    return {"status": "success", "company": company_name}

@router.get("/list-companies")
async def list_companies():
    """
    Returns a list of all registered companies (folders in DATA_STORAGE_PATH).
    """
    try:
        companies = [
            name for name in os.listdir(DATA_STORAGE_PATH)
            if os.path.isdir(os.path.join(DATA_STORAGE_PATH, name))
        ]
        return {"companies": companies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list companies: {str(e)}")