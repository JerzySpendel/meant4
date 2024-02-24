FROM python:3.11

RUN apt update -y
RUN apt upgrade -y

RUN mkdir /code
COPY requirements.txt /code

WORKDIR /code
RUN pip install -r requirements.txt

COPY src /code/src