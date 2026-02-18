# PDF to MCQ Generator API - Vercel Serverless Entry Point

import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mangum import Mangum
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    # Create minimal app for testing
    app = FastAPI(title="PDF to MCQ Generator API", version="1.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    @app.get("/api")
    @app.get("/api/")
    def health_check():
        return {"message": "PDF to MCQ Generator API", "version": "1.0.0", "status": "ok"}
    
    # Try to import and setup routes
    try:
        from config import MAX_FILE_SIZE
        from routes import setup_routes
        from handlers import setup_event_handlers, setup_exception_handlers
        
        setup_event_handlers(app)
        setup_exception_handlers(app)
        setup_routes(app)
    except ImportError as e:
        # Log but don't fail - at least health check will work
        print(f"Warning: Could not load full routes: {e}")
    
    # Export handler for Vercel
    handler = Mangum(app, lifespan="auto")
    
except Exception as e:
    print(f"FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    raise
