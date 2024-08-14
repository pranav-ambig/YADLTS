FROM python:3.10.8-alpine

ENV TZ=UTC

RUN apk --no-cache update && \
    apk --no-cache add \
        dos2unix \
        wget \
        python3 \
        tar \
        openjdk8-jre \
        py3-pip \
        bash \
        openrc \
        gcc \
        musl-dev \
        python3-dev \
        linux-headers

WORKDIR /app

COPY ./Distributed_Load_Testing_System /app/Distributed_Load_Testing_System
COPY ./Hosting_config/kafka.sh /app/
COPY requirements.txt /app/
COPY ./Hosting_config/config.sh /app/

RUN dos2unix /app/*.sh

RUN chmod +x /app/*.sh

EXPOSE 5000

CMD ["/bin/bash", "-c", "./config.sh"]
