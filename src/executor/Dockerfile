
# Docker file for the executor image
FROM python:3.12

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY execute.py execute.py

CMD ["python", "execute.py"]

