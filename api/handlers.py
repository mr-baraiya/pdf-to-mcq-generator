# Handle startup and errors

import os
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.utils.blob_storage import validate_blob_credentials

log = logging.getLogger(__name__)


def setup_event_handlers(app):
    # Skip startup events in serverless (Vercel)
    is_vercel = os.getenv("VERCEL") == "1"
    
    if is_vercel:
        log.info("Running on Vercel - skipping startup events")
        return
    
    # When app starts (local only)
    @app.on_event("startup")
    async def on_start():
        log.info("Starting API...")
        
        # Check if Vercel Blob is setup
        if validate_blob_credentials():
            log.info("Vercel Blob is ready")
        else:
            log.warning("Vercel Blob not configured - check .env file")


def setup_exception_handlers(app):
    # When error happens
    @app.exception_handler(Exception)
    async def handle_error(req, err):
        log.error(f"Error: {str(err)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Something went wrong"}
        )
