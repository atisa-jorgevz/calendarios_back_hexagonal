from fastapi import FastAPI
import logging

def configure_websockets(app: FastAPI):
    """Configure WebSocket routes on the main FastAPI application"""
    logger = logging.getLogger(__name__)
    try:
        # Import lazily to avoid import-time failures
        from app.interfaces.api.websocket_hitos import router as websocket_router
    except ModuleNotFoundError as e:
        logger.warning(f"WebSocket routes not loaded: {e}")
        return
    except Exception as e:
        logger.error(f"Error loading WebSocket routes: {e}")
        return

    app.include_router(websocket_router)
