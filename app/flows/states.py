from enum import Enum

class NOAState(str, Enum):
    INIT = "INIT"
    ASK_NAME = "ASK_NAME"
    ASK_GIRO = "ASK_GIRO"
    ASK_REDES = "ASK_REDES"
    ASK_PROBLEMA = "ASK_PROBLEMA"
    ANALYZE = "ANALYZE"
    RECOMMEND = "RECOMMEND"
    HANDOFF = "HANDOFF"
    CLOSED = "CLOSED"

class ConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Placeholder for FSM logic
        pass

    def get_state(self):
        pass

    def transition_to(self, next_state: NOAState):
        pass
