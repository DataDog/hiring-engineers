FROM python:3

WORKDIR /usr/src/app
COPY datadog.py ./

RUN pip install --no-cache-dir flask ddtrace
EXPOSE 5050/tcp

CMD ["ddtrace-run", "python3", "./datadog.py"]
