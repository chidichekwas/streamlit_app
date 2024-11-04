from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from decouple import config
from nodes.agent_state import AgentState


sys_msg = """
You are a report generator expert. Generate report in markdown format only.
"""

user_msg = """
    Say, I have a data frame with the following column definition:
    {df_columns}
    User asked a question: {query}
    Write a report on user's query in professional tone using plain and simple English. 
    Report should reflect only the answer of the user's query based on {execution_results} in Markdown format.
    Do not include any other text or your assumptions in the report.
    """

def generate_report(state: AgentState) -> AgentState:
    print("--- REPORT GENERATOR ---")

    OPENAI_API_KEY = config("OPENAI_API_KEY")
    GPT_MODEL = config("GPT_MODEL")

    query = state["query"]
    column_description = state["column_description"]
    execution_results = state["execution_results"]

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(sys_msg),
            HumanMessagePromptTemplate.from_template(user_msg),
        ]
    )
    llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = prompt | llm | StrOutputParser()
    reports = chain.invoke({"query": query, "execution_results": execution_results, "df_columns": column_description})

    return {
        "reports": reports
    }