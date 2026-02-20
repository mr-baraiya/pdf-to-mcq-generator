# All API endpoints/routes

import io
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException

from pdf.extractor import extract_text_from_pdf
from llm.mcq_generator import (
    generate_mcqs, 
    generate_with_ollama, 
    generate_with_groq, 
    generate_with_gemini,
    check_ollama_available
)
from utils.blob_storage import upload_pdf_to_blob, delete_pdf_from_blob
from utils.ollama_manager import (
    get_ollama_status,
    auto_install_ollama_linux,
    start_ollama_service
)
from models import MCQRequest, MCQResponse

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
    
    
    # Generate MCQ questions (Auto fallback: Ollama → Groq → Gemini)
    @app.post("/generate-mcqs", response_model=MCQResponse)
    async def make_mcqs(req: MCQRequest):
        try:
            log.info(f"Generating {req.num_questions} MCQs (Auto fallback)")
            qs = generate_mcqs(req.text, req.num_questions)
            log.info(f"Generated {len(qs)} questions")
            
            return {
                "questions": qs,
                "status": "success"
            }
        except Exception as e:
            log.error(f"Generate error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # Generate MCQ with LOCAL OLLAMA only
    @app.post("/generate-mcqs-ollama", response_model=MCQResponse)
    async def make_mcqs_ollama(req: MCQRequest):
        try:
            # Check if Ollama is available
            if not check_ollama_available():
                raise HTTPException(
                    status_code=503, 
                    detail="Ollama is not running. Start Ollama server first."
                )
            
            log.info(f"Generating {req.num_questions} MCQs with Ollama")
            qs = generate_with_ollama(req.text, req.num_questions)
            log.info(f"Generated {len(qs)} questions with Ollama")
            
            return {
                "questions": qs,
                "status": "success"
            }
        except HTTPException:
            raise
        except Exception as e:
            log.error(f"Ollama error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")
    
    
    # Generate MCQ with GROQ only
    @app.post("/generate-mcqs-groq", response_model=MCQResponse)
    async def make_mcqs_groq(req: MCQRequest):
        try:
            log.info(f"Generating {req.num_questions} MCQs with Groq")
            qs = generate_with_groq(req.text, req.num_questions)
            log.info(f"Generated {len(qs)} questions with Groq")
            
            return {
                "questions": qs,
                "status": "success"
            }
        except Exception as e:
            log.error(f"Groq error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Groq error: {str(e)}")
    
    
    # Generate MCQ with GEMINI only
    @app.post("/generate-mcqs-gemini", response_model=MCQResponse)
    async def make_mcqs_gemini(req: MCQRequest):
        try:
            log.info(f"Generating {req.num_questions} MCQs with Gemini")
            qs = generate_with_gemini(req.text, req.num_questions)
            log.info(f"Generated {len(qs)} questions with Gemini")
            
            return {
                "questions": qs,
                "status": "success"
            }
        except Exception as e:
            log.error(f"Gemini error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
    
    
    # Check which AI models are available
    @app.get("/ai-status")
    async def check_ai_status():
        """Check availability of AI models"""
        try:
            ollama_available = check_ollama_available()
            
            # Check Groq API key
            groq_key = os.getenv("GROQ_API_KEY")
            groq_available = bool(groq_key and groq_key.strip())
            
            # Check Gemini API key
            gemini_key = os.getenv("GEMINI_API_KEY")
            gemini_available = bool(gemini_key and gemini_key.strip())
            
            return {
                "ollama": {
                    "available": ollama_available,
                    "url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                    "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                    "description": "Local LLM - Free & Private"
                },
                "groq": {
                    "available": groq_available,
                    "model": "llama-3.3-70b-versatile",
                    "description": "Cloud LLM - Fast inference"
                },
                "gemini": {
                    "available": gemini_available,
                    "model": "gemini-2.0-flash",
                    "description": "Google AI - Advanced understanding"
                },
                "recommended": "ollama" if ollama_available else "groq"
            }
        except Exception as e:
            log.error(f"Status check error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # Get detailed Ollama status and installation info
    @app.get("/ollama-status")
    async def ollama_status():
        """Get Ollama installation and running status with instructions"""
        try:
            status = get_ollama_status()
            return status
        except Exception as e:
            log.error(f"Error checking Ollama status: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # Install Ollama (Linux only)
    @app.post("/ollama-install")
    async def install_ollama():
        """Auto-install Ollama (Linux only)"""
        try:
            status = get_ollama_status()
            
            if status["installed"]:
                return {
                    "success": True,
                    "message": "Ollama is already installed",
                    "installed": True,
                    "running": status["running"]
                }
            
            if not status["can_auto_install"]:
                return {
                    "success": False,
                    "message": f"Auto-install not available for {status['os']}",
                    "installation_instructions": status["installation_instructions"]
                }
            
            # Attempt installation on Linux
            result = auto_install_ollama_linux()
            return result
            
        except Exception as e:
            log.error(f"Installation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # Start Ollama service
    @app.post("/ollama-start")
    async def start_ollama():
        """Start Ollama service if installed"""
        try:
            result = start_ollama_service()
            if result["success"]:
                return result
            else:
                raise HTTPException(status_code=500, detail=result["message"])
        except Exception as e:
            log.error(f"Error starting Ollama: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
