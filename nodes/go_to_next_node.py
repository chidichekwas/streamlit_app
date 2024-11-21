from nodes.agent_state import AgentState


def go_to_next(state: AgentState):
    return state['next_node']