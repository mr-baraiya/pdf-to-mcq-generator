# PDF to MCQ Generator API

from mangum import Mangum
from api.config import create_app
from api.handlers import setup_event_handlers, setup_exception_handlers
from api.routes import setup_routes

# Create app
app = create_app()

# Add startup events
setup_event_handlers(app)

# Add error handlers
setup_exception_handlers(app)

# Add API routes
setup_routes(app)

# Vercel serverless handler
handler = Mangum(app, lifespan="off")
