FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYCODE 1

WORKDIR /app

COPY . /app/

RUN apt-get update

COPY requirement.txt .

RUN pip install -r requirement.txt


