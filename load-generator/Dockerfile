FROM locustio/locust
ADD locustfile.py locustfile.py

CMD locust  -H http://flask:5050 --no-web -c 10 -r 1
