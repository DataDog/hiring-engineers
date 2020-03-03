FROM python:3


WORKDIR /usr/src/app
COPY my-metric.py ./

RUN pip install --no-cache-dir datadog

CMD ["python3", "./my-metric.py"]
