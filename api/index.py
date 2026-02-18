# PDF to MCQ Generator API

import sys
import logging

# Setup logging first
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    from mangum import Mangum
    from api.config import create_app
    from api.handlers import setup_event_handlers, setup_exception_handlers
    from api.routes import setup_routes
    
    # Create app
    app = create_app()
    
    # Add startup events (skipped on Vercel)
    setup_event_handlers(app)
    
    # Add error handlers
    setup_exception_handlers(app)
    
    # Add API routes
    setup_routes(app)
    
    # Vercel serverless handler
    handler = Mangum(app, lifespan="auto")
    
    log.info("✓ API initialized successfully")
    
except Exception as e:
    log.error(f"✗ Failed to initialize API: {str(e)}")
    log.error(f"Error type: {type(e).__name__}")
    import traceback
    log.error(traceback.format_exc())
    raise
