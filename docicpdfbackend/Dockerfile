# Dockerfile
FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install pymupdf


COPY . /app/
