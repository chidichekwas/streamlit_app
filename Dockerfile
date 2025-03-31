FROM python:3.12

# This tells Docker to listen on port 80 at runtime. Port 80 is the standard port for HTTP.
EXPOSE  8501

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip
# install pip then packages
RUN pip3 install -r requirements.txt

# Create and activate virtual environment
#RUN python3 -m venv venv
#RUN . venv/bin/activate
# COPY requirements.txt .
#RUN pip install --upgrade pip

# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code into the container
COPY . .

ENV PIP_ROOT_USER_ACTION=ignore
# This copies everything in your current directory to the /app directory in the container.


HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]

