# All API endpoints/routes

import io
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException

from api.pdf.extractor import extract_text_from_pdf
from api.llm.mcq_generator import generate_mcqs
from api.utils.blob_storage import upload_pdf_to_blob, delete_pdf_from_blob
from api.models import MCQRequest, MCQResponse

log = logging.getLogger(__name__)


def setup_routes(app):
    
    # Health check
    @app.get("/")
    def home():
        return {
            "message": "PDF to MCQ Generator API",
            "version": "1.0.0"
        }
    
    
    # Upload PDF and extract text
    @app.post("/upload-pdf")
    async def upload_pdf(file: UploadFile = File(...)):
        try:
            # Check if PDF
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Upload PDF only")
            
            # Read file
            content = await file.read()
            
            # Upload to cloud storage
            log.info(f"Uploading: {file.filename}")
            blob = await upload_pdf_to_blob(content, file.filename)
            
            if not blob:
                raise HTTPException(status_code=500, detail="Upload failed")
            
            # Extract text from PDF
            try:
                pdf = io.BytesIO(content)
                text = extract_text_from_pdf(pdf)
                log.info(f"Extracted {len(text)} chars")
            except Exception as e:
                # Delete from cloud if extraction fails
                await delete_pdf_from_blob(blob.get("url"))
                raise HTTPException(status_code=500, detail=f"Extract failed: {str(e)}")
            
            return {
                "filename": file.filename,
                "text": text,
                "blob_url": blob.get("url"),
                "status": "success"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            log.error(f"Upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # Generate MCQ questions
    @app.post("/generate-mcqs", response_model=MCQResponse)
    async def make_mcqs(req: MCQRequest):
        try:
            log.info(f"Generating {req.num_questions} MCQs")
            qs = generate_mcqs(req.text, req.num_questions)
            log.info(f"Generated {len(qs)} questions")
            
            return {
                "questions": qs,
                "status": "success"
            }
        except Exception as e:
            log.error(f"Generate error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
