FROM python:3.5
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY ./scripts /tmp
COPY ./app /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["main.py"]
