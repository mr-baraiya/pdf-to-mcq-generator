import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

if os.getenv("VERCEL") != "1":
    load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

app = FastAPI(title="File to MCQ Generator API", version="1.0.0")

_frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
_allowed_origins = [o.strip() for o in _frontend_url.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_start():
    from blob_storage import validate_blob_credentials
    
    if validate_blob_credentials():
        log.info("Vercel Blob ready")
    else:
        log.warning("Vercel Blob not configured")

@app.exception_handler(Exception)
async def handle_error(req, err):
    log.error(f"Error: {str(err)}")
    return JSONResponse(status_code=500, content={"detail": "Something went wrong"})

from routes import setup_routes
setup_routes(app)
