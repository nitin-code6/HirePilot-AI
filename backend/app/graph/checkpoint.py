from typing import Dict, Any

class StateCheckpointService:
    """
    Checkpoint management service for persisting LangGraph conversation states.
    """
    _checkpoints = {}

    @classmethod
    def save(cls, session_id: str, state: Dict[str, Any]):
        cls._checkpoints[session_id] = state

    @classmethod
    def load(cls, session_id: str) -> Dict[str, Any]:
        return cls._checkpoints.get(session_id, {})
