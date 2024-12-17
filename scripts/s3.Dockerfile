FROM scality/s3server

WORKDIR /usr/src/app/

RUN echo "deb http://archive.debian.org/debian jessie main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security jessie/updates main" >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
    apt-get -o Acquire::AllowInsecureRepositories=true update && \
    apt-get -o Acquire::AllowInsecureRepositories=true install -y unzip && \
    apt-get clean
COPY data/postgres_data.zip data/postgres_data.zip
COPY data/s3_env.zip data/s3_env.zip
COPY scripts/unpack_s3_env.sh unpack_s3_env.sh
RUN chmod 777 unpack_s3_env.sh
RUN ./unpack_s3_env.sh
# CMD /bin/bash -c "./unpack_s3_env.sh"
