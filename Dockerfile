FROM python:3.12

EXPOSE  8501

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

RUN pip install --upgrade pip

# Create and activate virtual environment
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ./

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]

