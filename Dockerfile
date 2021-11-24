FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
