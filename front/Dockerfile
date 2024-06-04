# Dockerfile for Streamlit app

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/data 

CMD ["sh", "-c", "python -u src/db.py && streamlit run src/app.py"]