from functools import wraps
import time

from flask import Flask

from client import GenericClient

app = Flask(__name__)

client = GenericClient()


def grab_pageviews_and_latency(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        view_name = f.__name__
        start_time = time.time()
        resp = f(*args, **kwargs)
        end_time = time.time()
        client.update_pageviews_and_latency(view_name, end_time - start_time)
        return resp

    return wrapper


@app.route('/')
@grab_pageviews_and_latency
def hello_world():
    time.sleep(0.2)
    return 'Hello World!'


@app.route('/page1')
@grab_pageviews_and_latency
def page_one():
    time.sleep(0.5)
    return "Hello Stephen"


@app.route('/metrics')
def query_metrics():
    interval = 3600
    end = int(time.time())
    start = end - interval
    query = "avg:web.page_views{*}.as_count()"
    tags = ['page:hello_world', 'support']
    result = client.query(start, end, query, tags=tags)
    return result


if __name__ == '__main__':
    app.run()
