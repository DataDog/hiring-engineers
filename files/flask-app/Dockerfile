FROM python:alpine
ARG FLASK_APP
LABEL maintainer="tim.noeding@gmail.com"

RUN mkdir /code && \
    pip install --no-cache-dir flask blinker ddtrace

COPY flask-example.py /code/flask-example.py

WORKDIR /code

CMD nc -z dd 8126; sleep 10; python -m flask run --host=0.0.0.0
