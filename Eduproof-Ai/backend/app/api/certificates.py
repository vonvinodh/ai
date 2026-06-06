from fastapi import APIRouter, UploadFile, File, Form
import os
import shutil

from app.services.ocr_service import extract_text_from_pdf
from app.engines.credential_engine.authenticity_checker import analyze_certificate

router = APIRouter()
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/verify")
async def verify_certificate(file: UploadFile = File(...), resume_text: str | None = Form(None)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)
    verification = analyze_certificate(file_path, extracted_text, resume_text)

    return {
        "filename": file.filename,
        "verification": verification,
    }
