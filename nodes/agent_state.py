import pandas as pd
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class AgentState(TypedDict):
    # messages: Annotated[list[AnyMessage], add_messages]
    query: str
    is_query_relevant: bool
    rephrased_query: str
    csv_file_path: str
    column_description: str
    data_frame: pd.DataFrame
    Python_Code: str
    Python_script_check: int
    execution_error: str
    max_Python_script_check: int
    script_security_issues:str
    execution_results: str
    reports: str