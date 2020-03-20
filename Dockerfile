FROM python:3.7

RUN apt-get update &&\
    apt install mariadb-server

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt