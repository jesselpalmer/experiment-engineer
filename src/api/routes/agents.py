"""Agent execution API routes."""

from fastapi import APIRouter, HTTPException

from src.models.agent import AgentRequest, AgentResponse
from src.core.exceptions import AgentError
from src.core.registry import get_registry

router = APIRouter()


@router.post("/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest) -> AgentResponse:
    """Execute an agent with the given inputs.

    Args:
        request: Agent execution request

    Returns:
        Agent execution response

    Raises:
        HTTPException: If agent execution fails
    """
    registry = get_registry()

    try:
        # Get agent instance
        agent_kwargs = {}
        if request.config:
            if request.config.model:
                agent_kwargs["model"] = request.config.model
            if request.config.provider:
                agent_kwargs["provider"] = request.config.provider

        agent = registry.get_instance(request.agent_name, **agent_kwargs)

        # Execute agent
        result = agent.execute(**request.inputs)

        return AgentResponse(
            agent_name=request.agent_name,
            result=result,
            metadata={"status": "success"},
        )

    except AgentError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/list")
async def list_agents() -> dict[str, list[str]]:
    """List all available agents.

    Returns:
        Dictionary with list of agent names
    """
    registry = get_registry()
    return {"agents": registry.list_agents()}

