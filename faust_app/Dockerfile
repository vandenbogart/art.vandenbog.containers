FROM python:3.7-slim
    
RUN apt-get update && apt-get install -y wget && apt-get install -y git
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser


WORKDIR /app
COPY setup.py /app
RUN python3 setup.py develop

COPY . /app

ENTRYPOINT dockerize -wait tcp://kafka:9092 -timeout 60s faust_app worker -l info
