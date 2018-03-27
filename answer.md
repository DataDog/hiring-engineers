**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

![hostwithtags](https://user-images.githubusercontent.com/37661765/37962398-4179a2bc-31bb-11e8-9f31-b88bed7ae71b.png)

**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database:**

![mongodint](https://user-images.githubusercontent.com/37661765/37964835-2c497cde-31c3-11e8-9976-30013839fe15.png)

```
https://p.datadoghq.com/sb/e8083f4ea-53641cfa34821fe9cb8a10530203ad53
```

**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000:**

![mycustometric](https://user-images.githubusercontent.com/37661765/37965111-380f2e3c-31c4-11e8-89e4-2f2c16f86c18.png)

**Change your check's collection interval so that it only submits the metric once every 45 seconds:**

```
init_config:
  instances:
  - name: My first service
    url: mongodb://127.0.0.1:27017/
    timeout: 1
    min_collection_interval: 45
```

**Bonus Question Can you change the collection interval without modifying the Python check file you created? **

> _I don't think so_

**Your custom metric scoped over your host.**
```
   {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{host:mytestmachine.aidacool}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true,
  "status": "done"
}
```
**Any metric from the Integration on your Database with the anomaly function applied.**

  ```
 {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(avg:mongodb.connections.available{env:aidacool}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true
}
```

**Your custom metric scoped over your host.**

```
   {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{host:mytestmachine.aidacool}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true,
  "status": "done"
}
```

**Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket**

```
 {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:my_metric{role:test} by {host}.rollup(sum)",
      "type": "area",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true
}
```

![screenshot-2018-3-23 aida s timeboard 23 mar 2018 17 28 datadog](https://user-images.githubusercontent.com/37661765/37968497-97870268-31ce-11e8-8012-23bd18e8f25c.png)

![5mins](https://user-images.githubusercontent.com/37661765/37968534-b6d6272a-31ce-11e8-8c14-bab70f46dfba.png)
```
https://app.datadoghq.com/graph/embed?token=0d5b3609211aedcb51f30bdae831c1deeea8c025206ec72f05c26c8412836817&height=300&width=600&legend=false" width="600" height="300" frameborder="0"
```

```
https://app.datadoghq.com/graph/embed?token=27ee0c529aadcefebb23a8685f800d313efe4fbe89ae79406f2b0016cbca65de&height=300&width=600&legend=true" width="600" height="300" frameborder="0"
```

```
https://app.datadoghq.com/graph/embed?token=52c2c8a433b00fcae5db25fdbc6c745dd7f168d5152012db194d43c578c2aa88&height=300&width=600&legend=true" width="600" height="300" frameborder="0"
```

**Set the Timeboard's timeframe to the past 5 minutes**
![5mins](https://user-images.githubusercontent.com/37661765/37966034-74fa739e-31c7-11e8-966a-4dc4540d54a3.png)

**Take a snapshot of this graph and use the @ notation to send it to yourself.**
I seem unable to take a snapshot of the whole dashboard but only of each item.

![screenshot-2018-3-27 373 non letti - aidacool82 yahoo it - yahoo mail](https://user-images.githubusercontent.com/37661765/37970316-75b72802-31d3-11e8-8ed6-536e83ef532b.png)

**Bonus Question: What is the Anomaly graph displaying?**

> No Changes

![screenshot-2018-3-24 aida s timeboard 23 mar 2018 17 28 datadog](https://user-images.githubusercontent.com/37661765/37968684-1ce76380-31cf-11e8-8ac1-34ea4f1dd17a.png)

**Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:_
    Warning threshold of 500
    Alerting threshold of 800
    And also ensure that it will notify you if there is No Data for this query over the past 10m.**

![screenshot-2018-3-27 monitors datadog](https://user-images.githubusercontent.com/37661765/37970806-aea818a0-31d4-11e8-8a14-8e242a61fd0c.png)

```
{{is_alert}} my_metric average threshold has gone over  800 during past 5 minutes.  {{host.ip}} {{is_alert}}
{{is_warning}} my_metric average threshold has gone over 500 during past 5 minutes. {{is_warning}}
{{is_no_data}} No data for my_metric over the past 10m. {{is_no_data}}

@couliais@gmail.com
```

![screenshot-2018-3-24 datadog monitor created my_metric_monitor - couliais gmail com - gmail](https://user-images.githubusercontent.com/37661765/37971668-d0a3682c-31d6-11e8-86dc-e37082d71632.png)

**When this monitor sends you an email notification, take a screenshot of the email that it sends you.**

![screenshot-2018-3-24 monitor alert warn my_metric_monitor - couliais gmail com - gmail](https://user-images.githubusercontent.com/37661765/37967818-c2d64674-31cc-11e8-908c-962743ce00c0.png)

![screenshot-2018-3-27 monitor alert no data my_metric_monitor on role test - couliais gmail com - gmail](https://user-images.githubusercontent.com/37661765/37971583-9a3bf326-31d6-11e8-99e2-4862f67a2d13.png)

**Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
        One that silences it from 7pm to 9am daily on M-F,
        And one that silences it all day on Sat-Sun.
        Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification**

![screenshot-2018-3-24 338 non letti - aidacool82 yahoo it - yahoo mail](https://user-images.githubusercontent.com/37661765/37971474-4ffb5810-31d6-11e8-8b07-a48fa8a3a72f.png)

![screenshot-2018-3-24 337 non letti - aidacool82 yahoo it - yahoo mail](https://user-images.githubusercontent.com/37661765/37967869-e98dd642-31cc-11e8-82c0-208f64297803.png)

**Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:**

This seems not to be working. I have tried with different apps, with both the Agent 5 and 6 and also creating a new virtual environment but no traces or services displaying under APM on my UI. Here are the results that seem to indicate that all is good on my end.
 

```
2018-03-26 23:30:35 INFO (service_mapper.go:59) - total number of tracked services: 1
2018-03-26 23:31:35 INFO (service_mapper.go:59) - total number of tracked services: 1
2018-03-26 23:32:25 INFO (receiver.go:325) - no data received
2018-03-26 23:32:35 INFO (service_mapper.go:59) - total number of tracked services: 1
2018-03-26 23:33:31 INFO (trace_writer.go:89) - flushed trace payload to the API, time:744.798386ms, size:299 bytes
2018-03-26 23:33:35 INFO (receiver.go:325) - [lang:python lang_version:2.7.12 interpreter:CPython tracer_version:0.11.0] -> traces received: 2, traces dropped: 0, traces filtered: 0, traces amount: 524 bytes, services received: 1, services amount: 41 bytes
2018-03-26 23:33:35 INFO (service_mapper.go:59) - total number of tracked services: 1
2018-03-26 23:33:35 INFO (trace_writer.go:89) - flushed trace payload to the API, time:86.252612ms, size:298 bytes
2018-03-26 23:33:46 INFO (stats_writer.go:73) - flushed stat payload to the API, time:381.775773ms, size:405 bytes
2018-03-26 23:33:50 INFO (trace_writer.go:89) - flushed trace payload to the API, time:87.324552ms, size:301 bytes
2018-03-26 23:33:55 INFO (stats_writer.go:73) - flushed stat payload to the API, time:95.244016ms, size:406 bytes
2018-03-26 23:34:05 INFO (stats_writer.go:73) - flushed stat payload to the API, time:96.102812ms, size:410 bytes
2018-03-26 23:34:35 INFO (receiver.go:325) - [lang:python lang_version:2.7.12 interpreter:CPython tracer_version:0.11.0] -> traces received: 1, traces dropped: 0, traces filtered: 0, traces amount: 262 bytes, services received: 1, services amount: 41 bytes
```
```
from flask import Flask
import logging
import sys

#from ddtrace import tracer
#from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
#traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=True)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(port=3333)
```

```
DATADOG_SERVICE_NAME=aida-trace DATADOG_TRACE_DEBUG=true ddtrace-run  python myptest.py
DEBUG:ddtrace.commands.ddtrace_run:sys.argv: ['/home/aidacool/myproject/projects/venv/bin/ddtrace-run', 'python', 'myapptest.py']
DEBUG:ddtrace.commands.ddtrace_run:ddtrace root: /home/aidacool/myproject/projects/venv/local/lib/python2.7/site-packages/ddtrace
DEBUG:ddtrace.commands.ddtrace_run:ddtrace bootstrap: /home/aidacool/myproject/projects/venv/local/lib/python2.7/site-packages/ddtrace/bootstrap
DEBUG:ddtrace.commands.ddtrace_run:PYTHONPATH: /home/aidacool/myproject/projects/venv/local/lib/python2.7/site-packages/ddtrace/bootstrap
DEBUG:ddtrace.commands.ddtrace_run:sys.path: ['/home/aidacool/myproject/projects/venv/bin', '/home/aidacool/myproject/projects/venv/lib/python2.7', '/home/aidacool/myproject/projects/venv/lib/python2.7/plat-x86_64-linux-gnu', '/home/aidacool/myproject/projects/venv/lib/python2.7/lib-tk', '/home/aidacool/myproject/projects/venv/lib/python2.7/lib-old', '/home/aidacool/myproject/projects/venv/lib/python2.7/lib-dynload', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/home/aidacool/myproject/projects/venv/local/lib/python2.7/site-packages', '/home/aidacool/myproject/projects/venv/lib/python2.7/site-packages']
DEBUG:ddtrace.commands.ddtrace_run:program executable: /home/aidacool/myproject/projects/venv/bin/python
DEBUG:sitecustomize:skipping malformed patch instruction
DEBUG:ddtrace.monkey:failed to patch pyramid: module not installed
DEBUG:ddtrace.monkey:failed to patch aiopg: module not installed
DEBUG:ddtrace.monkey:failed to patch mysqldb: module not installed
DEBUG:ddtrace.monkey:failed to patch mysql: module not installed
DEBUG:ddtrace.monkey:failed to patch cassandra: module not installed
DEBUG:ddtrace.monkey:failed to patch redis: module not installed
DEBUG:ddtrace.monkey:failed to patch celery: module not installed
DEBUG:ddtrace.monkey:failed to patch pylibmc: module not installed
DEBUG:ddtrace.monkey:failed to patch pymongo: module not installed
DEBUG:ddtrace.monkey:failed to patch pylons: module not installed
DEBUG:ddtrace.monkey:failed to patch aiohttp: module not installed
DEBUG:ddtrace.monkey:failed to patch bottle: module not installed
DEBUG:ddtrace.monkey:failed to patch mongoengine: module not installed
DEBUG:ddtrace.monkey:failed to patch falcon: module not installed
DEBUG:ddtrace.monkey:failed to patch django: module not installed
DEBUG:ddtrace.monkey:failed to patch elasticsearch: module not installed
DEBUG:ddtrace.monkey:failed to patch psycopg: module not installed
INFO:ddtrace.monkey:patched 2/19 modules (flask,sqlite3)
DEBUG:ddtrace.tracer:set_service_info: service:aida-trace app:flask type:web
2018-03-26 23:33:47,339 - ddtrace.tracer - DEBUG - set_service_info: service:aida-trace app:flask type:web
DEBUG:ddtrace.writer:resetting queues. pids(old:None new:28718)
2018-03-26 23:33:47,339 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:28718)
DEBUG:ddtrace.writer:starting flush thread
2018-03-26 23:33:47,339 - ddtrace.writer - DEBUG - starting flush thread
INFO:werkzeug: * Running on http://127.0.0.1:3333/ (Press CTRL+C to quit)
2018-03-26 23:33:47,345 - werkzeug - INFO -  * Running on http://127.0.0.1:3333/ (Press CTRL+C to quit)
DEBUG:ddtrace.api:reported 1 services
2018-03-26 23:33:47,346 - ddtrace.api - DEBUG - reported 1 services
DEBUG:ddtrace.tracer:writing 1 spans (enabled:True)
2018-03-26 23:33:47,929 - ddtrace.tracer - DEBUG - writing 1 spans (enabled:True)
DEBUG:ddtrace.tracer:
      name flask.request
        id 838213091156984912
  trace_id 6360072546533132405
 parent_id None
   service aida-trace
  resource api_entry
      type http
     start 1522100027.93
       end 1522100027.93
  duration 0.002864s
     error 0
      tags 
           http.method:GET
           http.status_code:200
           http.url:http://localhost:3333/
           system.pid:28718
2018-03-26 23:33:47,929 - ddtrace.tracer - DEBUG - 
      name flask.request
        id 838213091156984912
  trace_id 6360072546533132405
 parent_id None
   service aida-trace
  resource api_entry
      type http
     start 1522100027.93
       end 1522100027.93
  duration 0.002864s
     error 0
      tags 
           http.method:GET
           http.status_code:200
           http.url:http://localhost:3333/
           system.pid:28718
INFO:werkzeug:127.0.0.1 - - [26/Mar/2018 23:33:47] "GET / HTTP/1.1" 200 -
2018-03-26 23:33:47,930 - werkzeug - INFO - 127.0.0.1 - - [26/Mar/2018 23:33:47] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00079s
2018-03-26 23:33:48,348 - ddtrace.api - DEBUG - reported 1 traces in 0.00079s
```

**Bonus Question: What is the difference between a Service and a Resource?**

A service is a set of processes that work together to allow the execution of a required operation.
The resource is a particular query to a service.

**Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.**

> The generate public URL doesn't seem to be active on dashboards on my account:

![aidanogeneratepublicurloption](https://user-images.githubusercontent.com/37661765/37965863-dec400fc-31c6-11e8-995f-d3fdd9fc3a33.png)

**Is there anything creative you would use Datadog for?**

I would use it to monitor the leaning rota at home
