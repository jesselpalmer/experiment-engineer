"""FastAPI application for ExperimentKit."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import router as v1_router
from src.core.logging import setup_logging

# Setup logging
setup_logging()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="ExperimentKit API",
        description="Agentic infrastructure for planning, running, and evaluating product experiments",
        version="0.1.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "ExperimentKit API", "version": "0.1.0"}

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app

