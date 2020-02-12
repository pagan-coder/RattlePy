FROM python:3.7-alpine3.8
MAINTAINER Premysl Lua Cerny

ENV LANG C.UTF-8

RUN set -ex \
	&& apk update \
	&& apk upgrade

RUN set -ex \
	&& apk add --virtual buildenvironment python3-dev \
	&& apk add --virtual buildenvironment libffi-dev \
	&& apk add --virtual buildenvironment openssl-dev \
	&& apk add --virtual buildenvironment gcc \
	&& apk add --virtual buildenvironment g++ \
	&& apk add --virtual buildenvironment musl-dev

RUN set -ex \
	&& pip install aiohttp

RUN apk del buildenvironment

RUN mkdir /opt
COPY ./rattlepy /opt/rattlepy
COPY ./rattlepy.py /opt/rattlepy.py

WORKDIR /opt
CMD ["python3", "/opt/rattlepy.py"]
