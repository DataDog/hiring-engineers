FROM python:3

WORKDIR /usr/src/app

RUN pip install datadog

COPY . .

CMD ["python", "./timeboard.py"]
