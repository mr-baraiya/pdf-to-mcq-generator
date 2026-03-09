import io
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from extractor import extract_text_from_pdf, extract_text_from_pptx, extract_text_from_txt
from mcq_generator import generate_mcqs
from blob_storage import upload_pdf_to_blob, delete_pdf_from_blob

log = logging.getLogger(__name__)


class MCQRequest(BaseModel):
    text: str
    num_questions: int = 5


class MCQResponse(BaseModel):
    questions: list
    status: str


def setup_routes(app):
    
    @app.get("/")
    def home():
        return {"message": "File to MCQ Generator API", "version": "1.0.0"}
    
    @app.post("/upload-file")
    async def upload_file(file: UploadFile = File(...)):
        try:
            is_pdf = file.content_type == "application/pdf" or file.filename.endswith(".pdf")
            is_pptx = file.content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation" or file.filename.endswith(".pptx")
            is_txt = file.content_type == "text/plain" or file.filename.endswith(".txt")
            
            if not is_pdf and not is_pptx and not is_txt:
                raise HTTPException(status_code=400, detail="Upload PDF, PPTX, or TXT only")
            
            content = await file.read()
            blob = await upload_pdf_to_blob(content, file.filename)
            
            try:
                file_stream = io.BytesIO(content)
                if is_txt:
                    text = extract_text_from_txt(file_stream)
                elif is_pptx:
                    text = extract_text_from_pptx(file_stream)
                else:
                    text = extract_text_from_pdf(file_stream)
            except Exception as e:
                if blob:
                    await delete_pdf_from_blob(blob.get("url"))
                raise HTTPException(status_code=500, detail=f"Extract failed: {str(e)}")
            
            return {
                "filename": file.filename,
                "text": text,
                "blob_url": blob.get("url") if blob else None,
                "status": "success"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            log.error(f"Upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.post("/generate-mcqs", response_model=MCQResponse)
    async def make_mcqs(req: MCQRequest):
        try:
            qs = generate_mcqs(req.text, req.num_questions)
            return {"questions": qs, "status": "success"}
        except Exception as e:
            log.error(f"Generate error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/ai-status")
    async def check_ai_status():
        try:
            groq_available = bool(os.getenv("GROQ_API_KEY"))
            return {
                "groq": {
                    "available": groq_available,
                    "model": "llama-3.3-70b-versatile"
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
