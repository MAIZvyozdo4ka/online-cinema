
FROM python:3.12-alpine

WORKDIR /code
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-client
COPY requirements.txt /code/requirements.txt

COPY install.sh /code/install.sh
COPY data/csv_data.zip /code/data/csv_data.zip
RUN chmod +x /code/install.sh
RUN sh /code/install.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini /code/alembic.ini