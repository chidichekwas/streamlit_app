FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Create and activate virtual environment
RUN python -m venv venv
RUN . venv/bin/activate
#RUN python3 -m pip install --upgrade pip

RUN pip install --upgrade pip --user

# install pip then packages
RUN pip install -r requirements.txt


# COPY requirements.txt .
#RUN pip install --upgrade pip

# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code into the container
COPY . .

#ENV PIP_ROOT_USER_ACTION=ignore
# This copies everything in your current directory to the /app directory in the container.


HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
# This tells Docker to listen on port 80 at runtime. Port 80 is the standard port for HTTP.
EXPOSE  8501

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]

