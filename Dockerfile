FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD ["python", "-c", "import streamlit; import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('localhost', 8501)); s.close()"]

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]
