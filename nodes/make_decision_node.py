from typing import Literal
from langgraph.graph import END
from nodes.agent_state import AgentState


def make_decision(state: AgentState) -> Literal[ "generate_report", "re_generate_python_code", END ]:
    print("--- MAKING DECISION ---")
    execution_error = state.get("execution_error", None)
    Python_script_check = state['Python_script_check']
    max_Python_script_check = state['max_Python_script_check']

    if execution_error:
        if Python_script_check >= max_Python_script_check:
            return END
        else:
            Python_script_check = Python_script_check + 1
            state.update({
                "Python_script_check": Python_script_check,
            })
            return "re_generate_python_code"
    else:
        return "generate_report"