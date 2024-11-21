import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.chat_models import ChatOllama
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from decouple import config
from nodes.agent_state import AgentState


sys_msg = """
        1. You are working with a pandas data frame called df in Python. Do not generate a new data frame. 
        2. The output of `print(df.head())` is:\n {df_head}.
        3. Only use the exact column names as specified in df_columns:\n {df_columns}.
        4. Avoid using any unauthorized column names not listed in df_columns.
        5. When creating the script, think about security, unauthorized access, resource usage, and avoiding any unnecessary external network connections.
        6. Respond with only the Python script in the correct syntax, without adding explanations.
        7. Generate a single output results as string and Print the output results using `print(...)`
    """

def generate_Python_code(state: AgentState) -> AgentState:
    print("--- PYTHON CODE GENERATOR ---")
    OPENAI_API_KEY = config("OPENAI_API_KEY")
    GPT_MODEL = config("GPT_MODEL")

    rephrased_query = state["rephrased_query"]
    rephrased_query = f"""
    {rephrased_query}
    Do it in Python and generate a single report. 
    Combine numerical analysis with observations, visualizations and charts.
    If any visualization is needed, save it in images folder with unique file name including uuid.
    Include the saved image with its RELATIVE PATH in the reports as markdown. 
    Generate the reports in markdown format (DO NOT INCLUDE ```markdown) and print the markdown reports.
    """
    csv_file_path = state["csv_file_path"]
    column_description = state["column_description"]
    df = pd.read_csv(csv_file_path)
    df_head = str(df.sample(10).to_markdown()) 

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(sys_msg),
            HumanMessagePromptTemplate.from_template(rephrased_query),
        ]
    )

    llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)

    chain = prompt | llm | StrOutputParser()
    
    code = chain.invoke({"df_head": df_head, "df_columns": column_description})

    return {
        "rephrased_query": rephrased_query,
        "Python_Code" : code,
        "data_frame": df,
    }