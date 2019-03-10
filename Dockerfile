FROM python:3.7.2-alpine3.9

RUN pip install flask ddtrace

WORKDIR /app
ADD app.py .

EXPOSE 5050

CMD ["ddtrace-run", "python", "app.py"]