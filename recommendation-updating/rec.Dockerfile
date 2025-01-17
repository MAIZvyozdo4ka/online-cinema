FROM python:3.12-slim


WORKDIR /code

COPY recommendation-updating/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
