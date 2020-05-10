FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5050

CMD gunicorn --bind 0.0.0.0:5050 wsgi:app
