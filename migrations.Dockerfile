
FROM python:3.12-alpine

WORKDIR /code
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-client
COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini /code/alembic.ini
