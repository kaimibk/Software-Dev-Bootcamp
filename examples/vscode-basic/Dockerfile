FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y sudo git

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
