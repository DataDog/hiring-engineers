# Steffen's answers

Hi<br>
my name is Steffen and I enjoyed runnning through this exercise. I was already
looking into some monitoring or visualization for my home automation system.<br>

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

I assume set up everything as described. The traces are produced from the app started like<br>
` * ddtrace-run flask run --port 5050 --host 0.0.0.0 &`

`*2018-11-26 12:33:48,267 - ddtrace.api - DEBUG - reported 1 traces in 0.01119s
INFO:werkzeug:192.168.27.1 - - [26/Nov/2018 14:20:47] "GET / HTTP/1.1" 200 -
2018-11-26 14:20:47,322 - werkzeug - INFO - 192.168.27.1 - - [26/Nov/2018 14:20:47] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.01557s
2018-11-26 14:20:47,640 - ddtrace.api - DEBUG - reported 1 traces in 0.01557s
INFO:werkzeug:192.168.27.1 - - [26/Nov/2018 14:20:49] "GET / HTTP/1.1" 200 -
2018-11-26 14:20:49,849 - werkzeug - INFO - 192.168.27.1 - - [26/Nov/2018 14:20:49] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00150s
2018-11-26 14:20:50,646 - ddtrace.api - DEBUG - reported 1 traces in 0.00150s`

# My comments

I liked the structure of the datadog.conf file. All default values have been entered and
umcommented like <br>```# enable_gohai: true```

I started a chat on the webpage to get some help. A case was opened and a case number and
link provided. As I am on the Europe instance it seems I am not able to login to the case tool
with my European account.

I had problems with the version 5.28 on my Raspberry to get the agent working with APM. Seems 
there are some details missing in the documentation. The configuration is mainly focusing on the 
datadog.yaml and nothing about the datadog.conf.



