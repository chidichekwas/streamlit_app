from typing import Literal
from pydantic import BaseModel, Field
from langgraph.graph import END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from decouple import config
from nodes.agent_state import AgentState


sys_msg = """
        1. You are working with a pandas DataFrame named `df` in Python.
        2. The structure (schema) of `df` is as follows: `{df_columns}`.
        3. Your task is to determine whether the user's query is relevant to this DataFrame.
        4. The user's query is: `{query}`.
    """




def check_query_relevancy(state: AgentState) -> AgentState:
    print("--- QUERY RELEVANCY CHECK ---")

    OPENAI_API_KEY = config("OPENAI_API_KEY")
    GPT_MODEL = config("GPT_MODEL")

    query = state["query"]
    column_description = state["column_description"]

    class grade(BaseModel):
        """Binary score for relevance check."""
        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model=GPT_MODEL, streaming=False, cache=False)

    llm_with_tool = model.with_structured_output(grade)

    prompt = PromptTemplate(
        template=sys_msg,
        input_variables=["df_columns", "query"],
    )

    chain = prompt | llm_with_tool 

    scored_result = chain.invoke(
        {"df_columns": column_description, "query": query}
    )
    grade = scored_result.binary_score

    if grade == "yes":
        return {"is_query_relevant" : True}
    else:

        return {"is_query_relevant": False}

