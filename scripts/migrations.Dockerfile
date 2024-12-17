FROM python:3.12-alpine

WORKDIR /code
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-client && apk add --no-cache bash

COPY requirements.txt /code/requirements.txt
COPY migration /code/migration

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini /code/alembic.ini

COPY data/postgres_data.zip /code/data/postgres_data.zip
COPY data/s3_env.zip /code/data/s3_env.zip
COPY scripts/unpack_migrations.sh /code/unpack_migrations.sh
RUN chmod 777 /code/unpack_migrations.sh
CMD /bin/bash -c "/code/unpack_migrations.sh \
                  && until pg_isready -U postgres -h postgres -p 5432; do echo Waiting for DB; sleep 2; done; alembic upgrade head"
