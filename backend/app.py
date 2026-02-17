from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import io
import logging
from dotenv import load_dotenv
from src.pdf.extractor import extract_text_from_pdf
from src.llm.mcq_generator import generate_mcqs
from src.utils.blob_storage import (
    upload_pdf_to_blob, 
    download_pdf_from_blob, 
    delete_pdf_from_blob,
    validate_blob_credentials
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF to MCQ Generator API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    logger.info("Starting PDF to MCQ Generator API...")
    
    # Check Vercel Blob credentials
    if validate_blob_credentials():
        logger.info("✓ Vercel Blob credentials configured")
    else:
        logger.warning(
            "⚠ Vercel Blob credentials not configured. "
            "PDF uploads will fail. Configure .env with:\n"
            "  VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_...\n"
            "  VERCEL_BLOB_STORE_ID=your_store_id"
        )

class MCQRequest(BaseModel):
    text: str
    num_questions: int = 5

class MCQResponse(BaseModel):
    questions: list
    status: str

@app.get("/")
def read_root():
    return {"message": "PDF to MCQ Generator API", "version": "1.0.0"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and extract text from PDF using Vercel Blob"""
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Vercel Blob
        blob_info = await upload_pdf_to_blob(file_content, file.filename)
        
        if not blob_info:
            raise HTTPException(status_code=500, detail="Failed to upload PDF to Vercel Blob")
        
        # Extract text from PDF (stored in memory)
        try:
            pdf_file = io.BytesIO(file_content)
            text = extract_text_from_pdf(pdf_file)
        except Exception as extract_error:
            # Cleanup blob if extraction fails
            await delete_pdf_from_blob(blob_info.get("url"))
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(extract_error)}")
        
        return {
            "filename": file.filename,
            "text": text,
            "blob_url": blob_info.get("url"),
            "blob_pathname": blob_info.get("pathname"),
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-mcqs", response_model=MCQResponse)
async def generate_mcqs_endpoint(request: MCQRequest):
    """Generate MCQs from given text"""
    try:
        questions = generate_mcqs(request.text, request.num_questions)
        return {
            "questions": questions,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
