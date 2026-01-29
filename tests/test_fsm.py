import pytest
from app.flows.states import ConversationManager, NOAState, sessions

def test_initial_state():
    user_id = "test_user_1"
    if user_id in sessions:
        del sessions[user_id]
    manager = ConversationManager(user_id)
    assert manager.get_state() == NOAState.INIT

def test_transition():
    user_id = "test_user_2"
    manager = ConversationManager(user_id)
    manager.transition_to(NOAState.ASK_NAME)
    assert manager.get_state() == NOAState.ASK_NAME

    manager.transition_to(NOAState.ASK_INDUSTRY)
    assert manager.get_state() == NOAState.ASK_INDUSTRY

def test_session_persistence():
    user_id = "test_user_3"
    manager1 = ConversationManager(user_id)
    manager1.transition_to(NOAState.ASK_PROBLEM)

    manager2 = ConversationManager(user_id)
    assert manager2.get_state() == NOAState.ASK_PROBLEM
