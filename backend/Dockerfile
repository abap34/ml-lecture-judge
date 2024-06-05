# Dockerfile for app
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/data 

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "python -u src/db.py && uvicorn src.main:app --host 0.0.0.0  --port 8000 --reload"]

