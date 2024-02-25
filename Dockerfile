FROM python:3.11

RUN apt update -y
RUN apt upgrade -y

RUN mkdir /code
COPY requirements.txt /code

WORKDIR /code
RUN pip install -r requirements.txt

COPY src /code/src
RUN mkdir images
CMD uvicorn --host 0.0.0.0 --port 8282 src.main:app