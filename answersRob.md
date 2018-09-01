## Robert King - Solutions Engineer Exercise

## Prerequisites - Setup the Environment

1. Downloaded and installed Docker and created a Linux, GNU container.

2. Downloaded Datadog Agent 6 which was installed into the container.

3. Registered on the Datadog website and retrieved an API Key.

4. In the container, an environment variable DD_API_KEY was created with the API Key used as the value. 

5. The Datadog portal hostmap graph showed the container.
[photo 1]

6. And the container metrics can be viewed on its dashboard.
[photo 2]


## Collecting Metrics

1. Used Bash to run commands in the GNU docker container:
- docker ps
- docker exec -it [containerid] /bin/bash

2. Downloaded and installed VI into the container:
- apt-get update
- apt-get install vim

3. Added the custom Agent tags to datadog.yaml
- cd /etc/datadog-agent/
- vi datadog.yaml
[photo 3]

4. The agent tags are displaying correctly on the Datadog host map.
[photo 4]

5. Install database on machine - I had MySQL already installed on my WINDOWS machine and so took the oppertunity to carryout the same steps above but for windows to understand any differences between the two setups.  I installed Agent 6 onto Windows and repeated the  steps listed above.  The custom agent tags were added to C:\ProgramData\Datadog\datadog.yaml for Windows.

6. I created the datadog user in the MySQL server with the specified privaledges and replication rights.

7. I edited the conf.d/mysql.d/conf.yaml allowing Datadog to access to the MySQL server:-

init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: bob
    options:
      replication: 0 
          
On an agent restart, Datadog then displayed the data collection for MySql metrics.
[Photo mysql installed]
[Photo - mysql data in dashboard]

8. To create the custom agent check I created my_metric.py in C:\ProgramData\Datadog\checks.d\
I imported the 'random' module into python, which enabled me to use the code: self.gauge('my_metric', random.randint(0,1000)) to create the random value.
[photo - custom agent check python code]

9. I then created the config yaml file, my_metric.yaml in C:\ProgramData\Datadog\conf.d\
I added the min_collection_interval metric at instance level (because it is Agent 6) and set the value to 45. 
[photo - custom agent check yaml file]

10. Bonus Question - An additional approach to modifying the collection interval is programatically by importing the time module and placing time.sleep(45) above the self.gauge() call.


## Visualizing Data

1. To create the Timeboard via the Datadog API I first created an application key within the portal.
[photo - timeboard apprlication key]

2. I installed the datadog module via PIP, enabling my timeboard code to compile:
- python -m pip install -u pip
- python -m pip install datadog

3. I then ran the timeboard.py code I created:
- python.exe timeboard.py

timeboard.py contains three graphs objects:- 
A. My_Metric
B. My_Metric rollup  
C. MySql number of connections

from datadog import initialize, api

options = {
    'api_key': '69e49857a99b3d228526cc96759369fc',
    'app_key': '8c3524a94f62d31d1181c099744d4843eb27d7d6'
}

initialize(**options)

title = "My Custom Timeboard"
description = "Timeboard for Datadog hiring process"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
			{"q": "avg:my_metric{host:DESKTOP-P8I3SKT}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_metric (random numbers) timeseries"
},
{
    "definition": {
        "events": [],
        "requests": [
			{"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL number of connections"
},
{
    "definition": {
        "events": [],
        "requests": [
			{"q": "avg:my_metric{host:DESKTOP-P8I3SKT}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My_metric rollup(sum) over 1 hour"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


4. After running the code the custom dashboard then appeared in the Datadog dashboard list
[photo - custom dashboard created via api]

[photo - The three graphs displaying on the dashboard]

5. The timeframe was set to the last 5 minutes by using the mouse to zoom in on the graph.
[photo - dashboard with 5 minute frequency]

6. I took a snapshot of the graph and sent it to myself via an @ annotation by clicking on the graph's camera icon
[photo of the @ annotation being sent to myself]

7. The anomaly graph shows the expected range of a selected metric, based on previous results. Any results that fall outside of this range are highlighted automatically, making it easier to spot and investigate anomalies.
            

## Monitoring Data

The My_metric monitor was setup using the following configuration:
[photo - monitoring settings]

And the custom email code is listed below:

{{#is_alert}}
ALERT! The metric has exceed the Alert Threshold
Metric value was: {{value}} 
Host IP: {{host.ip}}
{{/is_alert}}

{{#is_warning}}
Warning! The metric has exceed the Warning Threshold
{{/is_warning}}

{{#is_no_data}}
No data was received for my_metric
{{/is_no_data}} 

@loxwood7@googlemail.com @robert_king@email.com

[photo - email recieved for alert]

Downtime was also setup as specified, one of the recieved emails is shown below.

[photo - email recieved for downtime]


## Collecting APM Data

1. I first downloaded and installed the ddtrace module for Python:
- python -m pip install ddtrace

2. I then did the same for the flask module:
- python -m pip install flask

3. Within flaskapp.py I changed the host IP to 127.0.0.1

4. To get ddtrace-run to work in windows I added the ddtrace-run.exe path to my environment path.
- C:\Users\rob\AppData\Local\Programs\Python\Python37-32\Scripts

5. I could now run flaskapp.py via command line:
- ddtrace-run python flaskapp.py

6. The APM was now listening for traces, to generate data I visited the three application endpoints via a browser.
- 127.0.0.1:5050/
- 127.0.0.1:5050/api/apm
- 127.0.0.1:5050/api/trace

7. To add the APM data to my custom dashboard, which already contained infrastructure data, I clicked on the export icon on graphs I wanted to add.
[photo - export apm data to dashboard]

My custom dashboard displaying both infrastructure and APM data can be seen below.
[photo - custom dashboard with apm data]

8. Bonus Question

A "Service" is the name of a set of processes that work together. It deals with data and returns information that other programs or apps can consume when requested. An example of a web service would be an API.

A "Resource" is any information that is returned when querying a particular service. An example would a JSON object after a GET request for a service.

## Final Question 

To be updated.
