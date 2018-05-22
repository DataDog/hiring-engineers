FROM python:2.7.15-jessie

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apm-example.py ./
EXPOSE 5000
CMD [ "python", "./apm-example.py" ]
