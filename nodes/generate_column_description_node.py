import pandas as pd
from langchain_experimental.tools.python.tool import PythonAstREPLTool, PythonREPLTool
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.chat_models import ChatOllama
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from nodes.agent_state import AgentState
from decouple import config

sys_msg = """
    You are export on pandas data frame.
"""

user_msg = """
    I have data frame {df_head}. 
    Please generate description of each column in the following format:
    Name: The full name of the passenger.
    Provide only the column description.
"""

def generate_column_description(state: AgentState) -> AgentState:
    print("--- GENERATE COLUMN DESCRIPTION ---")

    OPENAI_API_KEY = config("OPENAI_API_KEY")
    GPT_MODEL = config("GPT_MODEL")

    csv_file_path = state["csv_file_path"]
    
    df = pd.read_csv(csv_file_path)

    df_head = str(df.head(5).to_markdown()) 

    prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(sys_msg),
                HumanMessagePromptTemplate.from_template(user_msg),
            ]
        )
    llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = prompt | llm | StrOutputParser()

    column_description = chain.invoke({"df_head": df_head}) 
    
    return {
        "column_description": column_description
    }