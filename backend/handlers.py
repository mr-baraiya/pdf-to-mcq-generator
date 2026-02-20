# Handle startup and errors

import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.blob_storage import validate_blob_credentials
from utils.ollama_manager import get_ollama_status

log = logging.getLogger(__name__)


def setup_event_handlers(app):
    # When app starts
    @app.on_event("startup")
    async def on_start():
        log.info("Starting API...")
        
        # Check if Vercel Blob is setup
        if validate_blob_credentials():
            log.info("✅ Vercel Blob is ready")
        else:
            log.warning("⚠️  Vercel Blob not configured - check .env file")
        
        # Check Ollama status
        try:
            status = get_ollama_status()
            
            if status["installed"] and status["running"]:
                log.info(f"✅ Ollama is ready ({status['model']})")
            elif status["installed"] and not status["running"]:
                log.warning(f"⚠️  Ollama installed but not running. Start with: POST /ollama-start")
            elif not status["installed"]:
                if status["can_auto_install"]:
                    log.warning(f"⚠️  Ollama not installed on {status['os']}. Auto-install with: POST /ollama-install")
                else:
                    log.warning(f"⚠️  Ollama not installed on {status['os']}. Visit: {status['installation_instructions']['manual_command']}")
        except Exception as e:
            log.error(f"Error checking Ollama status: {str(e)}")


def setup_exception_handlers(app):
    # When error happens
    @app.exception_handler(Exception)
    async def handle_error(req, err):
        log.error(f"Error: {str(err)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Something went wrong"}
        )
