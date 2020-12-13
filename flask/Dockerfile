FROM python:slim

RUN apt-get update && apt-get install -y wget && apt-get install -y git

WORKDIR /home
COPY setup.py /home
RUN python3 setup.py develop
COPY . /home/

ENV FLASK_APP=/home/app/main.py
ENV FLASK_ENV=development
EXPOSE 5000

ENTRYPOINT flask run --host 0.0.0.0