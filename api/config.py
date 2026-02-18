# App setup & configuration

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# File upload limits (Vercel serverless has 4.5MB limit, set to 3MB for safety)
MAX_FILE_SIZE = 3 * 1024 * 1024  # 3MB in bytes


def create_app():
    # Create FastAPI app
    app = FastAPI(
        title="PDF to MCQ Generator API",
        version="1.0.0"
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
