FROM python:slim

RUN apt-get update && apt-get install -y wget

# Dockerize install to wait on kafka tcp connection
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /home
COPY setup.py /home
RUN python3 setup.py develop
COPY . /home/

ENTRYPOINT dockerize -wait tcp://kafka:9092 -timeout 30s python3 -m consumer
