# PDF to MCQ Generator API

from config import create_app
from handlers import setup_event_handlers, setup_exception_handlers
from routes import setup_routes

# Create app
app = create_app()

# Add startup events
setup_event_handlers(app)

# Add error handlers
setup_exception_handlers(app)

# Add API routes
setup_routes(app)
