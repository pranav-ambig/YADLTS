FROM ubuntu:20.04

# Set the environment variable to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    dos2unix \
    wget \
    python3 \
    tar \
    openjdk-8-jdk\
    python3-pip

WORKDIR /app

COPY ./Distributed_Load_Testing_System /app/Distributed_Load_Testing_System
COPY ./Hosting_config/kafka.sh /app/
COPY requirements.txt /app/
COPY ./Hosting_config/config.sh /app/

RUN dos2unix /app/*.sh

RUN chmod +x /app/*.sh

EXPOSE 5000

CMD ["/bin/bash", "-c", "./config.sh"]
