FROM python:3-slim

ADD . /code
WORKDIR /code

RUN apt-get update -qq
RUN apt-get install gcc -y
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV PIETER_DB_HOST=redis
ENV PIETER_DB_PORT=6379
ENV PIETER_API_HOST=0.0.0.0
ENV PIETER_API_PORT=8000

CMD ["./pieter"]
