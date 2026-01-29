from enum import Enum
from typing import Dict

class NOAState(str, Enum):
    INIT = "INIT"
    ASK_NAME = "ASK_NAME"
    ASK_INDUSTRY = "ASK_INDUSTRY"
    ASK_SOCIAL_MEDIA = "ASK_SOCIAL_MEDIA"
    ASK_PROBLEM = "ASK_PROBLEM"
    ANALYZE = "ANALYZE"
    RECOMMEND = "RECOMMEND"
    HANDOFF = "HANDOFF"
    CLOSED = "CLOSED"

# In-memory session storage for development (Phase 1)
# user_id -> NOAState
sessions: Dict[str, NOAState] = {}

class ConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_state(self) -> NOAState:
        """Retrieves the current state for the user, defaults to INIT."""
        return sessions.get(self.user_id, NOAState.INIT)

    def transition_to(self, next_state: NOAState):
        """Updates the state for the user."""
        sessions[self.user_id] = next_state
