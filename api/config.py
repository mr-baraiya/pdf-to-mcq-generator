# App setup & configuration

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# File upload limits
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def create_app():
    # Detect if running on Vercel
    is_vercel = os.getenv("VERCEL") == "1"
    
    # Create FastAPI app
    app = FastAPI(
        title="PDF to MCQ Generator API",
        version="1.0.0",
        root_path="/api" if is_vercel else ""
    )
    
    # Allow frontend to call this backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    return app
