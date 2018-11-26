# Steffen's answers

Hi<br>
my name is Steffen and I enjoyed runnning through this exercise. I was already
looking into some monitoring or visualization for my home automation system. But, 
it was very easy and great documented to have a quick start. This challenge is quick
and great opportunity to dive into the product.<br>

# Environment
I have attached my home automation instance on a raspberry. There is no
binding for my Openhab installation, so I also tried to use home assistant
to transmit Smart Home information. In addition I added some data feeds via APIs<br>

## Collecting metrics
The screenshots show the hostmap after installing the agent to my Raspberry.
Hass means homeassitant, which is default naming by home assistance, not very clever in German language :-)
So, I changed the tag to \#homeassistant.

![ScreenShot](https://github.com/mod42/hiring-engineers/raw/master/screenshots/hostmap_details.png)

I added a Agent check that submits metric from my real home automation system (HAB). <br>
*	Temp_outside Temperature outside my house, direction North 

The additional metrics are added by a rule in my HAB once a day<br>
* HZ_usage-kWh the consumption of gas for heating in kWh<br>
* WW_Usage_kWh the consumption of gas for warm water in kWh<br>

Attached code and config is [house.py](src/house.py) and [house.yaml](src/house.yaml).

![Alt text](screenshots/openhab.png?raw=true "Openhab")

<b>Bonus question:</b> Is there another way to change the collection interval? <br>
 I was able to change the interval in the yaml.

## Visualizing Data

I used Paw on my Mac to execute the API call, please find the exported curl command here <br>
[Visualizing Data.sh](src/Visualizing_Data.sh)

My Timeboard (Past week)

 ![Alt text](screenshots/dashboard.png?raw=true "Dashboard")

The snapshot feature with the easy @ function is really great idea to quickly
save, send/inform others. Screenshots are a way more tideous. 

 ![Alt text](screenshots/snapshot.png?raw=true "Dashboard")


<b>Bonus Question:<b> What is the Anomaly graph displaying?<br>

I assume the Anomaly graph displace diviation from a band of expected values.
For my warm water heating, this would mean a high usage of energy. I had that in
the past, but without automatic chekcing. I found that one of the valve was broken,
whene the consumption rose by 50%, after a specific date. With this detector I would 
be alarmed earlier.

# Monitoring Data

![Alt text](screenshots/temp_step1+2.png?raw=true "temp_step1+2")


The code completion during writing the messages is really cool.

![Alt text](screenshots/alert_message.png?raw=true "alert_message")


![Alt text](screenshots/email_planned_downtime.png?raw=true "Email for planned downtime")

![Alt text](screenshots/alert_message.png?raw=true "alert_message")

# Collecting APM Data

I assume I have set up everything as described. The traces are produced from the app started like<br>
` ddtrace-run python my_app.py`

```shell
[root@playground ~]# ddtrace-run python test.py
 * Serving Flask app "test" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
DEBUG:ddtrace.api:reported 1 traces in 0.00716s
2018-11-26 15:29:20,217 - ddtrace.api - DEBUG - reported 1 traces in 0.00716s
DEBUG:ddtrace.api:reported 2 services
2018-11-26 15:29:20,218 - ddtrace.api - DEBUG - reported 2 services
2018-11-26 15:29:44,367 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
INFO:werkzeug:192.168.27.1 - - [26/Nov/2018 15:30:06] "GET / HTTP/1.1" 200 -
2018-11-26 15:30:06,212 - werkzeug - INFO - 192.168.27.1 - - [26/Nov/2018 15:30:06] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00220s
2018-11-26 15:30:06,404 - ddtrace.api - DEBUG - reported 1 traces in 0.00220s
INFO:werkzeug:192.168.27.1 - - [26/Nov/2018 15:30:14] "GET /api/apm HTTP/1.1" 200 -
2018-11-26 15:30:14,468 - werkzeug - INFO - 192.168.27.1 - - [26/Nov/2018 15:30:14] "GET /api/apm HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00116s
2018-11-26 15:30:15,414 - ddtrace.api - DEBUG - reported 1 traces in 0.00116s
INFO:werkzeug:192.168.27.1 - - [26/Nov/2018 15:30:19] "GET /api/trace HTTP/1.1" 200 -
2018-11-26 15:30:19,124 - werkzeug - INFO - 192.168.27.1 - - [26/Nov/2018 15:30:19] "GET /api/trace HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00140s
2018-11-26 15:30:19,419 - ddtrace.api - DEBUG - reported 1 traces in 0.00140s
```

I am able to see they are sent in the trace log `tail -f /var/log/datadog/trace-agent.log`

```shell
2018-11-26 15:30:09 INFO (trace_writer.go:97) - flushed trace payload to the API, time:477.941762ms, size:711 bytes
2018-11-26 15:30:19 INFO (trace_writer.go:97) - flushed trace payload to the API, time:478.874137ms, size:713 bytes
2018-11-26 15:30:24 INFO (trace_writer.go:97) - flushed trace payload to the API, time:488.77825ms, size:735 bytes
2018-11-26 15:30:24 INFO (stats_writer.go:265) - flushed stat payload to the API, time:504.857649ms, size:542 bytes
2018-11-26 15:30:33 INFO (api.go:324) - [lang:python lang_version:2.7.5 interpreter:CPython tracer_version:0.16.0] -> traces received: 3, traces dropped: 0, traces filtered: 0, traces amount: 6811 bytes, services received: 0, services amount: 0 bytes
2018-11-26 15:30:34 INFO (stats_writer.go:265) - flushed stat payload to the API, time:476.255178ms, size:757 bytes
2018-11-26 15:31:03 INFO (service_mapper.go:59) - total number of tracked services: 2
2018-11-26 15:31:39 INFO (trace_writer.go:97) - flushed trace payload to the API, time:638.438009ms, size:1261 bytes
2018-11-26 15:31:44 INFO (trace_writer.go:97) - flushed trace payload to the API, time:495.91676ms, size:712 bytes
2018-11-26 15:31:54 INFO (stats_writer.go:265) - flushed stat payload to the API, time:480.624009ms, size:564 bytes
```


But I am not able to see anything in the web console.
# Final Question

I think monitoring my house with Datadog would be a great thing. As I described above, monitoring
energy consumption and detecting anomalis is great for maintenance and savings. Alerts and events could
be used to signal errors like, the heating in a room is still on, but the sensor says the window
is open. That is for sure an error wasting energy and an error in the communication between the window
sensor and the heating actor (happens from time to time).   

# My observations

I started a chat on the webpage to get some help. A case was opened and a case number and
link provided. As I am on the Europe instance, it seems I am not able to login to the case tool
with my European account.

I had problems with the version 5.28 on my Raspberry to get the agent working with APM. Seems 
there are some details missing in the documentation. The configuration is mainly focusing on the 
datadog.yaml and nothing about the datadog.conf for the 5.* version. I have actived APM in the 
datadog.conf, but there was no process listening on 8126.

```shell
2018-11-26 16:31:57,333 - werkzeug - INFO - 192.168.0.46 - - [26/Nov/2018 16:31:57] "GET /api/trace HTTP/1.1" 200 -
ERROR:ddtrace.writer:cannot send spans to localhost:8126: [Errno 111] Connection refused
2018-11-26 16:31:57,806 - ddtrace.writer - ERROR - cannot send spans to localhost:8126: [Errno 111] Connection refused
```




