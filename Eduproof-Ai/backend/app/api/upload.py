from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.ocr_service import extract_text_from_pdf
from app.services.groc_service import analyze_resume

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    analysis = analyze_resume(extracted_text)

    return {
        "filename": file.filename,
        "analysis": analysis
    }