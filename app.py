import os
import io
import re
import json
import uuid 
import zipfile
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from graph_executer import get_reports, get_column_description
from file_manager_db import insert_file_info, get_all_file_info, update_column_description
from dotenv import load_dotenv, set_key

load_dotenv()

data_directory = os.path.join(os.path.dirname(__file__), "data")


# Initialize session states
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'last_report' not in st.session_state:
    st.session_state['last_report'] = None
if 'query' not in st.session_state:
    st.session_state['query'] = ''
if 'selected_dataset_name' not in st.session_state:
    st.session_state['selected_dataset_name'] = None
if 'editable_column_description' not in st.session_state:
    st.session_state['editable_column_description'] = ''
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None  # Store the DataFrame directly in session state
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = os.getenv("OPENAI_API_KEY", "")
if 'gpt_model' not in st.session_state:
    st.session_state['gpt_model'] = os.getenv("GPT_MODEL", None)

def update_env_variable(key, value):
    env_path = ".env"
    set_key(env_path, key, value)

def sanitize_filename(query):
    # Remove special characters and limit filename length
    sanitized = re.sub(r'[^a-zA-Z0-9_\- ]', '', query)  # Allow only alphanumeric, underscore, hyphen, and space
    sanitized = "_".join(sanitized.split())  # Replace spaces with underscores
    return sanitized[:50]  # Limit to 50 characters for readability

def download_png_files(png_paths):
    png_files = {}
    for path in png_paths:
        try:
            with open(path, 'rb') as f:
                png_files[Path(path).name] = f.read()
        except FileNotFoundError:
            st.warning(f"File {path} not found")
            
    return png_files

def download_reports(query, report):
    markdown_content = f"# Query: {query}\n\n{report}"
    markdown_file = io.StringIO(markdown_content)  # Use StringIO to create an in-memory file
    filename = sanitize_filename(query) + ".md"
    download_key = str(uuid.uuid4())
    st.download_button(
        label="Download Report as Markdown",
        data=markdown_file.getvalue(),
        file_name=filename,
        mime="text/markdown",
        key=download_key
    )

def download_reports_with_png(query, report):
    # Extract PNG file paths from the markdown report
    pattern = r'!\[.*?\]\((.*?\.png)\)'
    png_paths = re.findall(pattern, report)
    
    # Download or collect PNG files
    png_files = download_png_files(png_paths)

    # Create a ZIP file in-memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add markdown report to the ZIP
        markdown_content = f"# Query: {query}\n\n{report}"
        markdown_filename = sanitize_filename(query) + ".md"
        zip_file.writestr(markdown_filename, markdown_content)

        # Add PNG files to the ZIP
        for file_name, content in png_files.items():
            zip_file.writestr(file_name, content)

    zip_buffer.seek(0)  # Move the buffer pointer to the start

    # Offer the ZIP file as a download
    zip_filename = sanitize_filename(query) + ".zip"
    download_key = str(uuid.uuid4())
    st.download_button(
        label="Download Report",
        data=zip_buffer,
        file_name=zip_filename,
        mime="application/zip",
        key=download_key
    )

def update_headings(text):
    # Replace headings in the order from largest to smallest to prevent conflicts
    text = re.sub(r'(?m)^###### ', '####### ', text)  # Handle heading 6, if any
    text = re.sub(r'(?m)^##### ', '###### ', text)
    text = re.sub(r'(?m)^#### ', '##### ', text)
    text = re.sub(r'(?m)^### ', '#### ', text)
    text = re.sub(r'(?m)^## ', '### ', text)
    text = re.sub(r'(?m)^# ', '## ', text)
    return text

def display_reports(markdown_text):
    # Regex to find image references and capture captions and paths
    image_pattern = r'!\[(.*?)\]\((.*?)\)'

    # Split the markdown text into segments by images
    parts = re.split(image_pattern, markdown_text)

    # Find all image references to extract their captions and paths
    image_matches = re.findall(image_pattern, markdown_text)

    # Display the content and images alternately
    text_index = 0

    if len(image_matches) == 0:
        # No images found, display the full markdown text at once
        st.markdown(markdown_text)
    else:
        # Proceed with the original loop logic if there are images
        for i in range(len(parts)):
            if i % 3 == 0:
                st.markdown(parts[i])
            elif i % 3 == 1:
                if text_index < len(image_matches):
                    caption, path = image_matches[text_index]
                    if os.path.exists(path):
                        st.image(path.strip(), caption=caption)
                    text_index += 1

def submit_query():
    if st.session_state['last_report']:
        st.session_state['history'].append(st.session_state['last_report'])

    selected_name = st.session_state['selected_dataset_name']
    if selected_name:
        available_datasets = get_all_file_info()
        dataset_info = next(((path, column_description) for name, path, column_description in available_datasets if name == selected_name), None)
        dataset_path, column_description = dataset_info

        if dataset_path:
            try:
                with st.spinner("Generating report..."):
                    st.session_state['query'] = st.session_state['query_input']
                    report = get_reports(st.session_state['query'], dataset_path, column_description)
                    report = update_headings(report)
                    st.session_state['last_report'] = (st.session_state['query'], report)
            except Exception as e:
                st.error(f"Error occurred: {e}")
        else:
            st.error("Selected dataset not found.")
    else:
        st.warning("Please select a dataset.")

    st.session_state['query'] = ''

# Title of the app
st.title("Question Answering on CSV Files")

def data_analysis_content():
    st.subheader("Select Dataset for Analysis")
    
    if not all([st.session_state['openai_api_key'], st.session_state['gpt_model']]):
        st.info("First Configure OpenAI API Key and Model Name in the 'Configuration' tab. After that, upload and name a CSV file in the 'Load CSV' tab.")
    else:
        available_datasets = get_all_file_info()
        if available_datasets:
            dataset_choices = [name for name, _, _ in available_datasets]
            st.selectbox("Choose a dataset:", dataset_choices, key="selected_dataset_name", index=None)
        else:
            st.info("No datasets available. Please upload and name a CSV file in the 'Load CSV' tab.")

    if st.session_state['selected_dataset_name']:
        with st.form(key='query_form'):
            query = st.text_input("Enter your query:", value=st.session_state['query'], key="query_input")
            submit_button = st.form_submit_button(label="Generate Report", on_click=submit_query)

        if st.session_state['last_report']:
            query, report = st.session_state['last_report']
            st.markdown(f"## Query: {query}")
            display_reports(report)
            download_reports_with_png(query, report)

        st.subheader("Chat History")
        total_history = len(st.session_state['history']) 
        for i, (query, report) in enumerate(reversed(st.session_state['history'])):
            st.markdown(f"## Query {total_history - i}: {query}")
            display_reports(report)
            download_reports_with_png(query, report)
    else:
        st.info("Please select a dataset for analysis.")


def load_csv_content():
    st.subheader("Configure Datasets")

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    dataset_name = st.text_input("Dataset Name")

    if st.button("Add Dataset"):
        if uploaded_file and dataset_name:
            try:
                save_path = os.path.join(data_directory, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load and store DataFrame and column description in session state
                st.session_state['dataframe'] = pd.read_csv(save_path)
                st.session_state['editable_column_description'] = get_column_description(save_path)
                
                results = insert_file_info(dataset_name, save_path, st.session_state['editable_column_description'])
                results = json.loads(results)

                if results['success']:
                    st.success(results['message'])
                else:
                    st.error(results['message'])
            except Exception as e:
                st.error(f"Error loading CSV: {e}")
        else:
            st.warning("Please upload a CSV file and provide a dataset name.")

    # Check if dataframe and column description are loaded in session state
    if st.session_state['dataframe'] is not None and st.session_state['editable_column_description']:
        # Display DataFrame first
        st.dataframe(st.session_state['dataframe'].sample(10))
        
        # Display editable column description below
        updated_description = st.text_area(
            "Edit Column Description",
            value=st.session_state['editable_column_description'],
            height=250
        )

        # Submit updated column description
        if st.button("Update Column Description"):
            update_result = update_column_description(dataset_name, updated_description)
            update_result = json.loads(update_result)
            if update_result["success"]:
                st.success("Column description updated successfully!")
                st.session_state['editable_column_description'] = updated_description
            else:
                st.error(update_result["message"])


def configuration_content():
    st.subheader("Configuration")

    # Input fields for API key and model name
    api_key_input = st.text_input("OpenAI API Key", value=st.session_state['openai_api_key'], type="password")
    model_options = ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4"]
    model_name_input = st.selectbox("OpenAI Model Name", options=model_options, index=model_options.index(st.session_state['gpt_model']) if st.session_state['gpt_model'] in model_options else None)
    def save_configuration():
        # Update session state with the new configuration values
        st.session_state['openai_api_key'] = api_key_input
        st.session_state['gpt_model'] = model_name_input
        update_env_variable("OPENAI_API_KEY", api_key_input)
        update_env_variable("GPT_MODEL", model_name_input)
        load_dotenv()
        st.success("Configuration saved successfully!")

    # Save configuration button with the callback function
    st.button("Save Configuration", on_click=save_configuration)


# Tab structure
tab1, tab2, tab3 = st.tabs(["Data Analysis", "Load CSV", "Configuration"])

with tab1:
    data_analysis_content()
with tab2:
    load_csv_content()
with tab3:
    configuration_content()

    
