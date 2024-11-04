from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from decouple import config
from nodes.agent_state import AgentState

# llm = ChatOllama(
#     model="llama3.2",
#     temperature=0,
# )

df_columns = """
    PassengerId: A unique identifier for each passenger.
    Survived: Indicates whether the passenger survived (1) or not (0).
    Pclass: Passenger class (1st, 2nd, or 3rd class).
    Name: The full name of the passenger.
    Sex: The gender of the passenger (male or female).
    Age: The age of the passenger in years.
    SibSp: The number of siblings or spouses aboard the Titanic.
    Parch: The number of parents or children aboard the Titanic.
    Ticket: The ticket number of the passenger.
    Fare: The fare paid for the ticket.
    Cabin: The cabin number where the passenger stayed.
    Embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton).
"""

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

    # print(f"Execution Results: {execution_results}\n")

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(sys_msg),
            HumanMessagePromptTemplate.from_template(user_msg),
        ]
    )
    llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = prompt | llm | StrOutputParser()
    reports = chain.invoke({"query": query, "execution_results": execution_results, "df_columns": column_description})

    # print(f"Generated Report:\n{reports}\n")

    return {
        "reports": reports
    }