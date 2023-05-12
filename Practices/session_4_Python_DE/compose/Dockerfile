FROM python:3.10-slim

ENV PYTHONBUFFERED 1

RUN apt-get update -y

RUN mkdir project
WORKDIR project

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src /project/
COPY ./resources /project/resources