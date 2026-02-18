# PDF to MCQ Generator API - Vercel Serverless Entry Point

from mangum import Mangum
from api.config import create_app
from api.handlers import setup_event_handlers, setup_exception_handlers
from api.routes import setup_routes

# Create FastAPI app
app = create_app()

# Setup handlers (conditional for Vercel)
setup_event_handlers(app)
setup_exception_handlers(app)

# Setup routes
setup_routes(app)

# Export handler for Vercel
handler = Mangum(app, lifespan="auto")
