FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app
RUN pip install --upgrade pip
RUN pip install ddtrace
