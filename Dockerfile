FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code into the container
COPY . .

# This command creates a .streamlit directory in the home directory of the container.
RUN mkdir ~/.streamlit

# This copies your Streamlit configuration file into the .streamlit directory you just created.
RUN cp config.toml ~/.streamlit/config.toml

ENV PIP_ROOT_USER_ACTION=ignore
# This copies everything in your current directory to the /app directory in the container.

# This tells Docker to listen on port 80 at runtime. Port 80 is the standard port for HTTP.
EXPOSE  8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]

