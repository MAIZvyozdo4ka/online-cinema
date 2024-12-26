
FROM python:3.12-alpine

WORKDIR /code
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-client
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev
COPY migration/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-client g++
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini /code/alembic.ini
