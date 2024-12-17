FROM python:3.12-alpine

RUN apk add --no-cache bash && apk add --no-cache bash unzip

WORKDIR /usr/src/app

COPY data/s3_env.zip data/s3_env.zip
COPY data/postgres_data.zip data/s3_env.zip
COPY scripts/unpack_env.sh /init.sh

RUN chmod +x /init.sh

CMD /bin/bash -c "/init.sh"
