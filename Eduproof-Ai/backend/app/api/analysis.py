from fastapi import APIRouter, UploadFile, File, Form
import os
import shutil

from app.services.ocr_service import extract_text_from_pdf
from app.engines.content_engine.content_analysis import analyze_resume_content

router = APIRouter()
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/content")
async def analyze_content(
    file: UploadFile = File(...),
    github_url: str | None = Form(None),
    portfolio_text: str | None = Form(None),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)
    analysis = analyze_resume_content(extracted_text, github_url, portfolio_text)

    return {
        "filename": file.filename,
        "analysis": analysis,
    }
