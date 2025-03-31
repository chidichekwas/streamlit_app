FROM python:3.12

EXPOSE  8501

WORKDIR /app

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py",  "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]

