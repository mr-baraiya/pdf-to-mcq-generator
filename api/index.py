from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Create app
app = FastAPI(title="PDF to MCQ Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes after app creation
try:
    from config import MAX_FILE_SIZE
    from routes import setup_routes
    from handlers import setup_event_handlers, setup_exception_handlers
    
    setup_event_handlers(app)
    setup_exception_handlers(app)
    setup_routes(app)
except Exception as e:
    print(f"Warning loading routes: {e}")
    # Fallback health check
    @app.get("/api")
    @app.get("/api/")
    def health():
        return {"message": "PDF to MCQ Generator API", "version": "1.0.0"}

# Vercel entry point
async def handler(request: Request):
    from mangum import Mangum
    asgi_handler = Mangum(app, lifespan="off")
    return await asgi_handler(request.scope, request.receive, request._send)
