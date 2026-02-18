# App setup & configuration

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env file (only for local, Vercel uses env vars)
if os.getenv("VERCEL") != "1":
    load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# File upload limits
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def create_app():
    try:
        # Detect if running on Vercel
        is_vercel = os.getenv("VERCEL") == "1"
        log.info(f"Environment: {'Vercel' if is_vercel else 'Local'}")
        
        # Create FastAPI app (no root_path for Vercel)
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
        
        log.info("✓ FastAPI app created successfully")
        return app
        
    except Exception as e:
        log.error(f"✗ Failed to create app: {str(e)}")
        raise
