from langgraph.graph import START, StateGraph, END
from langgraph.graph.graph import CompiledGraph

from nodes.query_relevancy_check_node import check_query_relevancy
from nodes.make_decision_based_on_query_relevant_node import make_decision_on_query_relevancy
from nodes.query_relevancy_report_node import query_relevancy_report
from nodes.query_re_write_node import re_write_query
from nodes.Python_code_generator_node import generate_Python_code
from nodes.Python_code_sanitize_node import sanitize_python_script
from nodes.Python_code_executer_node import run_python_code
from nodes.re_generate_Python_script import re_generate_Python_code
from nodes.report_generator_node import generate_report
from nodes.make_decision_node import make_decision
from nodes.agent_state import AgentState


def generate_graph()-> CompiledGraph:
    
    workflow = StateGraph(AgentState)
    workflow.add_node("check_query_relevancy", check_query_relevancy)
    workflow.add_node("query_relevancy_report", query_relevancy_report)
    workflow.add_node("re_write_query", re_write_query)
    workflow.add_node("generate_python_code", generate_Python_code)
    workflow.add_node("execute_python_code", run_python_code)
    workflow.add_node("re_generate_python_code", re_generate_Python_code)
    workflow.add_node("generate_report", generate_report)

    workflow.add_edge(START, "check_query_relevancy")
    
    workflow.add_conditional_edges(
        "check_query_relevancy",
        make_decision_on_query_relevancy,
    )

    workflow.add_edge("re_write_query", "generate_python_code")

    workflow.add_conditional_edges(
        "generate_python_code",
        sanitize_python_script,
    )
    workflow.add_conditional_edges(
        "execute_python_code",
        make_decision,
    )
    workflow.add_edge("re_generate_python_code", "execute_python_code")
 
    workflow.add_edge("query_relevancy_report", END)
    workflow.add_edge("generate_report", END)

    graph = workflow.compile()

    try:
        graph.get_graph(xray=1).draw_mermaid_png(output_file_path="pandas_dataframe_qa.png")
    except ValueError as e:
        print(f"Failed to generate graph image: {e}")
        print("Consider using an alternative visualization method or checking your network connection.")
    
    return graph



