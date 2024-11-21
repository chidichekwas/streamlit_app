from typing import Literal
from nodes.agent_state import AgentState

def make_decision_on_query_relevancy(state: AgentState) -> Literal[ "re_write_query", "query_relevancy_report" ]:
    print("--- MAKE DECISION BASED ON QUERY RELEVANCY ---")

    is_query_relevant = state["is_query_relevant"]

    if is_query_relevant:
        return "re_write_query"
    else:
        return "query_relevancy_report"