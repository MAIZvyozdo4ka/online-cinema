FROM python:3.12-slim

RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY s3-init/ /code/s3-init

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY scripts/create_movie_csv.sh /app/create_movie_csv.sh
RUN chmod 777 /app/create_movie_csv.sh
CMD /bin/bash -c "/app/create_movie_csv.sh"