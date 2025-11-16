"""API v1 routes."""

from fastapi import APIRouter

from src.api.routes import agents, workflows

router = APIRouter()

# Include route modules
router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])

