# Dockerfile for Streamlit app

FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /app

CMD ["streamlit", "run", "app.py"]

