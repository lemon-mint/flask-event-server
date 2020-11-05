FROM alpine:latest

RUN apk update
RUN apk add python3
RUN apk add py3-pip

ADD . /app
WORKDIR /app

RUN python3 -m pip install -r requirement.txt

EXPOSE 9064
CMD python3 app.py
