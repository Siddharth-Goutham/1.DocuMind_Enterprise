from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os

from app.services.pdf_service import process_pdf
from app.services.vector_service import add_documents

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "backend/uploads")

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        docs = process_pdf(file_path)
        add_documents(docs, user_id)

        return {"message": "PDF uploaded and processed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
