FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano python3-dev build-base linux-headers pcre-dev gcc
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install pip==18.1
RUN pip install -r /var/www/requirements.txt
