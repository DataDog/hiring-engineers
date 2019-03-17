FROM python:3

RUN pip install flask
RUN pip install ddtrace

COPY app.py /app.py
EXPOSE 5050
CMD ddtrace-run python /app.py