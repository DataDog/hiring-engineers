## Robert King - Solutions Engineer Exercise

## Prerequisites - Setup the Environment

1. I downloaded and installed Docker and created a Linux, GNU container.

2. I then downloaded Datadog Agent 6 and installed it into the container.

3. Registering on the Datadog website I was then able to retrieved an API Key.

4. In the container, I created an environment variable DD_API_KEY, using the API Key as the value. 

5. The Datadog portal hostmap graph showed the container.
<img src="https://image.ibb.co/eE5jnz/1_linux_docker_data_visible.png" />

6. And the container metrics can be viewed on its dashboard.
<img src="https://image.ibb.co/f7KASz/photo_2_custom_dashboard.png" />


## Collecting Metrics

1. I used Bash to run commands in the GNU docker container:
- docker ps
- docker exec -it [containerid] /bin/bash

2. Then downloaded and installed VI into the container:
- apt-get update
- apt-get install vim

3. The custom Agent tags were added to datadog.yaml
- cd /etc/datadog-agent/
- vi datadog.yaml
<img src="https://image.ibb.co/j0MeLK/photo_3_linux_datadog_yaml.png" />

4. The agent tags are displaying correctly on the Datadog host map.
<img src="https://image.ibb.co/gC84nz/photo_4_tags_added_to_linux_docker.png" />

5. Install database on machine - I had MySQL already installed on my WINDOWS machine and so took the opportunity to carry out the same steps above but for windows to understand any differences between the two setups.  I installed Agent 6 onto Windows and repeated the steps listed above.  The custom agent tags were added to C:\ProgramData\Datadog\datadog.yaml for Windows.

6. I created the datadog user in the MySQL server with the specified privileges and replication rights.

7. I edited the conf.d/mysql.d/conf.yaml allowing Datadog to access to the MySQL server:-

init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: bob
    options:
      replication: 0 
          
On an agent restart, Datadog then displayed the data collection of MySQL metrics.
<img src="https://image.ibb.co/mxrPnz/photo_mysql_installed.png"/>
<img src="https://image.ibb.co/mO5TEe/photo_mysql_data_dashboard.png"/>

8. To create the custom agent check I created my_metric.py in C:\ProgramData\Datadog\checks.d\
I imported the 'random' module into python, which enabled me to use the code: self.gauge('my_metric', random.randint(0,1000)) to create the random value.
<img src="https://image.ibb.co/jDgPnz/photo_my_metric_python_code.png"/>

9. I then created the config yaml file, my_metric.yaml in C:\ProgramData\Datadog\conf.d\
I added the min_collection_interval metric at instance level (because it is Agent 6) and set the value to 45. 
<img src="https://image.ibb.co/nosaue/photo_my_metric_yaml_code.png"/>

10. Bonus Question - An additional approach to modifying the collection interval is programmatically by importing the time module and placing time.sleep(45) above the self.gauge() call.


## Visualizing Data

1. To create the timeboard via the Datadog API I first created an application key within the portal.
<img src="https://image.ibb.co/b0UzLK/photo_timeboard_api_application_key.png"/>

2. I installed the datadog module via PIP, enabling my timeboard code to compile:
- python -m pip install -u pip
- python -m pip install datadog

3. I then ran the timeboard.py code I created:
- python.exe timeboard.py

timeboard.py contains three graphs objects:- 
A. My_Metric
B. My_Metric rollup  
C. MySQL number of connections

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
<img src="https://image.ibb.co/dgZoEe/photo_custom_dashboard_created_via_api.png"/>

<img src="https://image.ibb.co/cxpc7z/photo_custom_dashboard_all_metrics.png"/>

5. The timeframe was set to the last 5 minutes by using the mouse to zoom in on the graph.
<img src="https://image.ibb.co/gZpzLK/photo_custom_dashboard_over_5_minutes.png"/>

6. I took a snapshot of the graph and sent it to myself via an @ annotation by clicking on the graph's camera icon
<img src="https://image.ibb.co/bxPoEe/photo_snapshot_of_dashboard.png"/>

7. The anomaly graph shows the expected range of a selected metric, based on previous results. Any results that fall outside of this range are highlighted automatically, making it easier to spot and investigate anomalies.

There are three different anomaly detection algorithms: 
- Basic, can be used when data has no repeatable seasonal pattern.  The Basic algorithm is quick to execute and react because it uses less data by not considering longer trends.  An example business that would be best suited to the Basic algorithm is online gambling. 

- Agile, can be used for data that contains seasonal trends and you want the algorithm to quickly react to level shifts.  The Agile algorithm only uses immediate past data and so won't consider anomalies with a longer duration making it potentially less robust.  The majority of retail businesses would best suit the Agile algorithm.

- Robust, is best used for seasonal trend data that doesn't significantly fluctuate.  Robust will consider long lasting anomalies and so be slower to identify level shifts but produce stable predictions overtime.  Financial services and public sector websites would likely suit the Robust algorithm the most.
            

## Monitoring Data

The My_metric monitor was setup using the following configuration:
<img src="https://image.ibb.co/fOP27z/photo_monitor_settings.png"/>

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

<img src="https://image.ibb.co/n2kvue/photo_email_from_alert.png"/>

Downtime was also setup as specified, one of the recieved emails is shown below.

<img src="https://image.ibb.co/dvgqSz/photo_email_for_downtime.png"/>


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
<img src="https://image.ibb.co/k8dgZe/photo_export_apm_graph_to_timeboard.png"/>

My custom dashboard displaying both infrastructure and APM data can be seen below.
https://app.datadoghq.com/dash/898727/my-custom-timeboard?live=true&page=0&is_auto=false&from_ts=1535200544582&to_ts=1535805344582&tile_size=m
<img src="https://image.ibb.co/bWQTEe/photo_custom_dashboard_with_apm_data_added.png"/>

8. Bonus Question

A Service is a collection of processes that work together to do the same job.  Some service examples are; an API service, a database service and a web application service.  Datadog automatically assigns services one of four types; web, database, cache and custom.

A Resource is a request for a particular action of a service to run.  A couple examples of a resource are; a query string for a database to execute, and a URL request of a web application service.


## Final Question 

The continual advancement in technology excites me. And the emergence of the Internet of Things (IOT) now presents a plethora of monitoring possibilities! Nest Smart Thermostat, Alexa, Wearables, Connected Cars, home security systems, shipping, health care, the list is endless!

These services use the internet to connect with endpoints and request and receive data. Those endpoints and the infrastructure they sit on will require monitoring. What would happen if hospital staff lose the ability to track assets — staff members, patients and hardware — throughout the building? Employee frustration, patient dissatisfaction, bad publicity, loss of data, loss of life... Ensuring adequate monitoring coverage can prevent bad situations like these from happening! Datadog monitoring can help keep customers happy, make businesses money and even save lives!

These IOT services can also integrate with each other. For example, The Blink home security system can integrate with Alexa, users can now configure and arm their security systems through voice recognition. Pretty cool!

So, businesses, in addition to their own monitoring, now need to consider monitoring their integrations. I’d advocate that both businesses have monitoring, policing the other business, ensuring they also provide a good service, particularly if there are SLA’s to consider. If an integration can be implemented in many different flavours, then the end user experience is also increasingly important.

Understanding what the end user is experiencing from a range of different browsers, devices (is estimated that there will be 30 billion devices by 2020 world-wide)[1] and different GEO locations will enable the business to setup comprehensive testing, prioritising the devices and browsers that their users use the most.

Synthetic or real user monitoring data would complement Datadog’s wealth of data. Synthetic and real user monitoring will provide insight into the end user experience, both from a UI and a ‘perception of performance’ perspective. Is this a back-end or front-end problem? Is a website slower on a particular browser/device? How many users are using this browser/device? How much revenue is this bad experience costing the business? How can this issue be fixed?

It is also vital that businesses know about problems before their customers tell them. And with the use of anomaly detection algorithms, it is now possible to prevent problems from happening ahead of time by making use of collected historical data.

So rather than a single, unique Datadog monitoring opportunity, I see limitless options, and as a Solutions Engineer, I’d love to sell Datadog to every single one!


1. https://spectrum.ieee.org/tech-talk/telecom/internet/popular-internet-of-things-forecast-of-50-billion-devices-by-2020-is-outdated

