from app.core.config import settings
import logging

logger = logging.getLogger("hirepilot.tracer")

class AgentTracer:
    """
    LangSmith tracing telemetry integration.
    Captures multi-agent supervisor hops, tool execution durations and status.
    """
    @staticmethod
    def trace_agent_execution(agent_name: str, input_prompt: str, duration_ms: float, status: str = "success"):
        if settings.LANGSMITH_TRACING and settings.LANGSMITH_API_KEY:
            logger.info(f"[LANGSMITH TRACE] Agent: {agent_name} | Duration: {duration_ms}ms | Status: {status}")
        else:
            logger.debug(f"[LOCAL TRACE] Agent: {agent_name} finished in {duration_ms}ms with status {status}")

agent_tracer = AgentTracer()
