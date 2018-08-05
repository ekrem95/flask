FROM python:3.6-alpine

RUN apk add --update alpine-sdk
RUN apk add "libffi-dev=3.2.1-r4"
RUN apk add "postgresql-dev=10.4-r0"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000
CMD [ "python", "./app.py" ]