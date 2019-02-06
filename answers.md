Your answers to the questions go here.

# COLLECTING METRICS:

***Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> see "1.Tags.JPG" Screencap  http://52.233.42.140/1.Tags.JPG
    
***Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  
> see "2.MySQL.JPG" Screencap http://52.233.42.140/2.MySQL.JPG
    
***Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    
    > SAMPLE CODE
        from datadog_checks.checks import AgentCheck
        __version__ = "1.0.0"
        from random import *
        class mycheck(AgentCheck):
        def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
    
***Change your check's collection interval so that it only submits the metric once every 45 seconds.
    
    > added to my_metrics.yaml
        init_config:
        instances:
        - min_collection_interval: 45
    
***Bonus Question Can you change the collection interval without modifying the Python check file you created?
    
    > ANSWER: Yes by modifying the collection interval in the YAML file (my_metric.yaml)
        instances:
        - min_collection_interval: 45
           
# VISUALIZING DATA:

***Utilize the Datadog API to create a Timeboard that contains:
  
*Your custom metric scoped over your host.

    > SAMPLE CODE
    from datadog import initialize, api
    options = {
    'api_key': '651af2f85fe1b1e4fdc86f49a8c9e786',
    'app_key': '93b2db04c9890eeebfb57b83222a11f274ffbb26'
    }
    initialize(**options)
    title = "My API Timeboard - My Metric"
    description = "An informative timeboard."
    graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:DATADOGVM}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Timeboard"
    }]
    template_variables = [{
    "name": "DATADOGVM",
    "prefix": "host",
    "default": "host:DATADOGVM"
    }]
    read_only = True
    api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


*Any metric from the Integration on your Database with the anomaly function applied.

    > SAMPLE CODE
    from datadog import initialize, api
    options = {
    'api_key': '651af2f85fe1b1e4fdc86f49a8c9e786',
    'app_key': '93b2db04c9890eeebfb57b83222a11f274ffbb26'
    }
    initialize(**options)
    title = "My API Timeboard - MySQL Anomalies"
    description = "An informative timeboard."
    graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL CPU Performance Anomalies"
    }]
    template_variables = [{
    "name": "DATADOGVM",
    "prefix": "host",
    "default": "host:DATADOGVM"
    }]
    read_only = True
    api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


*Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

    > SAMPLE CODE
    from datadog import initialize, api
    options = {
    'api_key': '651af2f85fe1b1e4fdc86f49a8c9e786',
    'app_key': '93b2db04c9890eeebfb57b83222a11f274ffbb26'
    }
    initialize(**options)
    title = "My API Timeboard - My Metric"
    description = "An informative timeboard."
    graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:DATADOGVM}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "My Metric Bucket"
    }]
    template_variables = [{
    "name": "DATADOGVM",
    "prefix": "host",
    "default": "host:DATADOGVM"
    }]
    read_only = True
    api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


***Once this is created, access the Dashboard from your Dashboard List in the UI:

*Set the Timeboard's timeframe to the past 5 minutes
 
> see "9.Timeframe.JPG" Screencap http://52.233.42.140/9.Timeframe.JPG
 
*Take a snapshot of this graph and use the @ notation to send it to yourself.

> see "10.Notation.JPG" Screencap http://52.233.42.140/10.Notation.JPG

> see "10.Notation-Email.JPG" Screencap http://52.233.42.140/10.Notation-Email.JPG

*Bonus Question: What is the Anomaly graph displaying?

   > ANSWER: The deviance +/- (bounds) from the average over the dataset.

# MONITORING DATA:

***Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

    *Warning threshold of 500
    *Alerting threshold of 800
    *And also ensure that it will notify you if there is No Data for this query over the past 10m.
    
> see "11.Monitor.png" Screencap http://52.233.42.140/11.Monitor.png

***Please configure the monitor’s message so that it will:

    *Send you an email whenever the monitor triggers.
    *Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
    *Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
    *When this monitor sends you an email notification, take a screenshot of the email that it sends you.

> see "11.EmailNotification.JPG" Screencap http://52.233.42.140/11.EmailNotification.JPG

***Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
   
    *One that silences it from 7pm to 9am daily on M-F,
    *And one that silences it all day on Sat-Sun.
    *Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

> see "12.Downtime.JPG" Screencap http://52.233.42.140/12.Downtime.JPG

> see "12.DowntimeEmail.JPG" Screencap http://52.233.42.140/12.DowntimeEmail.JPG

# VISUALIZING DATA:

***Bonus Question: What is the difference between a Service and a Resource?

   > A: The differences primarily break down to hierarchy, where a service encompases many resources which may in turn be elements of processes.
   Services may comprise many processes that are all geared toward the same purpose - eg: a website may be backed by a web process and a database process.
   Resources are a subset of a process - a database query is a resource of a database process which in turn is an element of a service

***Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

> https://app.datadoghq.com/dashboard/rf2-afu-sfj/daves-dashboard

> see "12.DowntimeEmail.JPG" Screencap http://52.233.42.140/12.DowntimeEmail.JPG
     
***Please include your fully instrumented app in your submission, as well.
   
    > SAMPLE CODE
    from ddtrace import tracer, patch
    tracer.configure(hostname='agent', port='8126')
    patch(requests=True)
    import requests
    @tracer.wrap(name='get-python-jobs', service='get-jobs')
    def get_sites():
     homepages = []
     span = tracer.current_span() 
     res = requests.get('https://jobs.github.com/positions.json?description=python')
     span.set_tag('jobs-count', len(res.json()))
     for result in res.json():
        print('Getting website for %s' % result['company'])
        try:
            res = requests.get(result['company_url'])
            homepages.append(res)
        except Exception as err:
            print('Unable to get site for %s' % result['company'])
    return homepages
    a = get_sites()


# FINAL QUESTION:

> Realitime metrics on energy usage overlaid with time of day rates. This would be a compelling way to provide a visual on optimal time to use energy and appreciate how much energy is used locally.

> Tracking temperature! With historical data, it would be possible to overlay historical metrics to give context to current temperature levels - in addition to seeing current trends, having historical data overlaid would make for a very interesting visual.
