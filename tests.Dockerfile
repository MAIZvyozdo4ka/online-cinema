FROM python:3.12-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY tests /code/tests
COPY core /code/core
COPY admin_service /code/admin_service
COPY auth_service /code/auth_service
COPY moderator_service /code/moderator_service
COPY movie_service /code/movie_service
COPY rating_service /code/rating_service
COPY review_service /code/review_service
COPY user_service /code/user_service