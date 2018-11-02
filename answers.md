## Introduction and Getting Started
Working on this exercise was definitely an insightful journey. This made me learn a lot about the DataDog solution itself and more importantly how the technology is working behind the scenes. The opensource nature of this product really makes DataDog a robust solution out in the market for infrastructure and application monitoring.
I decided to implement this exercise on my local environment (Windows 10). I did run into some dependency issues here and there but I was able to overcome them to successfully complete all the steps in the exercise. My findings are below:

## Collecting Metrics
The installation of the DataDog Agent itself was very straight forward. It is worth noting that the Agent itself has everything embedded inside of it. All the checks, integrations, python interpreter, etc. Yet the Agent is very lightweight. Small code snippet of the DataDog yaml file is below which shows the 3 tags I created. Followed by a screenshot of the Host Map in the DataDog UI. By adding tags to your metrics you can observe and alert on metrics from different hardware profiles, software versions, availability zones, services, roles or any other level you may require. Tags give you the flexibility to add infrastructural metadata to your metrics on the fly without modifying the way your metrics are collected.

*Tags in the Datadog.yaml file*

    tags:
      - env:windows
      - host:HIBBJQHEQJ
      - region:AMS
    use_dogstatsd: true

*DataDog Host View Map Screenshot*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/HostMapView1.png)

The tags reside in the DataDog's Agent yaml file. However, it is not necessary to open the yaml file every time to make a change to the configuration. The changes can also be made by directly launching the DataDog Agent Manager UI and navigating to the settings tab. The settings tab displays the yaml file and changes can be made directly there and saved. Once the changes are made, restart the Agent for the changes to take effect.

To integrate with a database, I went ahead with installing PostgreSQL on my local environment and configured the respective yaml file in the postgres.d folder within the DataDog Agent. To successfully integrate with DataDog, proper permissions for a user are needed. So I created a user 'datadog' with proper permissions. The configured yaml file is below:

*postgres.yaml*

    #postgres.yaml
    init_config:

    instances:
     - host: localhost
       port: 5432
       username: datadog
       password: Password1
       tags:
         - postgres
      
Once the configuration is set, I restarted the DataDog Agent. To view if DataDog was connected and collecting metrics from my postgres, I checked the 'Collector Status' from the DataDog Agent Manager. Please see the screenshot below:

*Postgres Status Screenshot*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/PostgresStatus.png)

Creating custom agent check is actually a very nifty task. However, a multitude of integrations are offered OOTB but it is simple to write a check to monitor something if it is not offered OOTB. Writing a custom python integration script to integrate it with DataDog just shows how flexible its opensource architecture is. It is very simple yet very powerful. A few things need to be kept in mind however while creating a custom agent check. For example, both .yaml and .py files must be of same name, otherwise DataDog will not pick up the configuration of the check. I created a separate folder in the conf.d folder called 'my_metric.d' where I stored the my_metric.yaml file. Next, I created the my_metric.py file to store it in the 'checks.d' folder embedded within the DataDog Agent folder. Below is the code for my_metric.yaml and my_metric.py to implement the custom agent check.

*my_metric.yaml*
    
    #my_metric.yaml
    
    init_config:
    metric_prefix: my_metric

    instances:
    #[{}]
    - username: mo
      min_collection_interval: 45
     
     
*my_metric.py*

    #my_metric.py
    
    __version__ = "1.0.0"
    
    import random
    from checks import AgentCheck
    
    class my_metric(AgentCheck):
        def check(self, instance):
            metric_prefix = self.init_config.get('metric_prefix', 'my_metric')
            randomValue = random.randint(0, 1000)
            self.gauge('my_metric', randomValue)
    
#### Bonus Question: Can you change the collection interval without modifying the Python check file you created?
Yes, the collection interval can be changed in the .yaml file with the minimum_collection_interval setting as shown in the my_metric.yaml code above.

## Visualizing Data
DataDog's Timeboard is a useful utility when it comes to visualizing data. The Timeboard provides many different options as to how you can customize your view of data. I have posted the screenshot below of the Timeboard created via DataDog Timeboard API and the code is below as well.

*Timeboard via API Screenshot*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/CustomTimeboardviaAPI.png)

*Timeboard API code*

    from datadog import initialize, api

    options = {
        'api_key': 'a6ab84e20b5b3b1dfc1ea12796bdfa04',
        'app_key': '544c72dc1a84d3426b3042a483fb648df5760d50'
     }

    initialize(**options)

    title = "Mo Timeboard Created Via API"
    description = "Mo Timeboard Created Via API"
    graphs = [{
             "title": "avg:my_metric{host:HIBBJQHEQJ}",
             "definition": {
                 "events": [],
                 "requests": [
                     {"q": "avg:my_metric{host:HIBBJQHEQJ}"}
                  ]
              },
            "viz": "timeseries"
          },
          {
          "title": "anomalies(avg:postgresql.max_connections{host:HIBBJQHEQJ}, 'basic', 2)",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.max_connections{host:HIBBJQHEQJ}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
         },
 
          {
          "title": "avg:my_metric{host:HIBBJQHEQJ}.rollup(sum, 3600)",
          "definition": {
              "events": [],
              "requests": [
				    {
				      "q": "avg:my_metric{host:HIBBJQHEQJ}.rollup(sum, 3600)",
				      "style": {
				        "palette": "dog_classic",
				        "type": "solid",
				        "width": "normal"
				      },
				      "conditional_formats": [],
				      "aggregator": "sum"
				    }
              ],
              "viz": "query_value"
          }
          
        }]

    tv = [{
        "name": "host1",
        "prefix": "host",
        "default": "host:HIBBJQHEQJ"
    }]
    read_only = False
    api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=tv,
                     read_only=read_only)

Also, I have posted the screenshot below of the anomaly snapshot taken of the 5 minute timeframe from the custom Timeboard graph.

*Anomaly Snapshot of 5 Mins Time Lapse Screenshot*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/PostgresAnomaly5minsGraph.png)

#### Bonus Question: What is the Anomaly graph displaying?
The Anomaly graph is displaying the Postgres max_connections metric with an unusual spike that is outside of the standard deviation bounds.

## Monitoring Data
It is always good to know how overall infrastructure and applications are doing in terms of performance. Especially if they are critical to the business. Applications that generate a lot of revenue for an organization should be monitored very closely and of course the infrastructure where the application is sitting as well. DataDog's monitoring capabilities make it very simple and intuitive for anyone to start monitoring the metrics around the infrastructure and application. The monitor configurations also allow for users to schedule downtimes for alerts if the user does not want to be disturbed off hours for example; or notify on the spot if the data has gone missing for a few consecutive minutes. Please find the screenshots below:

*Screenshot below of creating and configuring the monitors*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/CreatingMonitors.png)

*Screenshot below of whenever a monitor is triggered and an email notification is received*     
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MonitorTriggeredEmailNotification.png)

*Screenshot below of monitor alert email notification when an alert is triggered for metric above 800. Provides the value of the sample and the host IP. Metric value is showing as 829.5*     
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MetricAlertEmailNotification.png)

#### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
*Screenshot of downtime scheduled in DataDog for 7pm - 9am on Mon-Fri*    
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/ScheduledDowntimeForOffHours.png)

*Screenshot of downtime scheduled in DataDog for all day weekends*      
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/ScheduledDowntimeForWeekends.png)

*Screenshot of downtime scheduled email notification received when downtime was scheduled*       
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/DowntimeScheduledEmailNotification.png)

*Screenshot of downtime started email notification received when downtime started*       
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/DowntimeStartedEmailNotification.png)

## Collecting APM Data
It is very critical to deliver an application into production with extreme quality. Organizations invest blood, money, and sweat to develop and deliver robust and quality applications. Investing in good tools for functional testing, performance testing, and tools that can give full visibility into application lifecycle are very critical. But what about once the application is released into production? Is it not equally important, if not more, to keep monitoring the performance of that application once it is delivered in the hands of the end user? From my perspective, it is MORE important to monitor how the application is performing out in the real world. When an organization tests the application before its release, they test the application with basic use cases assuming how the end user may react with the application. But the reality is, we cannot restrict the actions of end users and cannot limit them to using the application in a specific manner, which is why it becomes very critical to monitor the application and its performance after it is in production.
With DataDog's APM solution, it becomes very flexible to instrument the application with DataDog's tracer. DataDog APM supports a number of frameworks and technologies OOTB. DataDog offers a couple of neat ways to instrument the applications - automatic instrumentation or manual instrumentation. Below is a Flask application instrumented manually with DataDog's tracer followed by a public URL of DataDog's Dashboard with both APM and Infrastructure metrics.

*APM Configuration in Datadog.yaml file*

    apm_config:
      enabled: true
      receiver_port: 8126
      apm_non_local_traffic: true

*Flask Application Instrumentation With ddtrace*

    from flask import Flask
    import blinker as _

    from ddtrace import tracer
    from ddtrace.contrib.flask import TraceMiddleware

    app = Flask(__name__)

    traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

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
        app.run(host='0.0.0.0', port='5050')
    
Please find the link below to the public URL of my DataDog Dashboard. The application will need to be executed via cmd or terminal and then navigate to 0.0.0.0:5050 to input requests for data to populate in the Timeboard and Dashboard. I have also included screenshots below of my APM Timeboard, custom dashboard, and APM flame graph. Please view the screenshots below:

*DataDog Dashboard Public URL*   
(https://p.datadoghq.com/sb/5a3d8d1c0-861d08d9512c0fb276dfc7dc625ee24e)

*My Flask App Flame Graph Screenshot*   
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/APMFlameGraph.png)

*My Flask App In DataDog Screenshot*   
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyFlaskAppInDatadog.png)

*My Flask App Service Screenshot*   
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyFlaskAppService.png)

*My Custom Screenboard With APM and Infrastructure Metrics Screenshot*   
![Alt text](https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyCustomScreenboard.png)

#### Bonus Question: What is the difference between a Service and a Resource?
In the context of APM, a service is a set of processes or software that provide a set of functionality. A resource is a subset of a service or a particular action catered to that service. A service can have many individual resources. For example, www.datadog.com is a whole service provided to a user. When a user logs into their account by going to www.datadog.com/login, that 'login' functionality serves as an endpoint resource to that service.

## Final Question - Is there anything creative you would use DataDog for?
Given the flexibility, robustness, and opensource architecture of DataDog, I can think of many creative ways DataDog can be applied to real life scenarios. A good one would be to monitor the very obvious correction that is happening in the market. Stocks are dropping because of uncertainty in the elections, the tarrifs, and other factors played. The point being, it would be really neat to monitor the trends and analysis of the market's ups and downs to make educated decisions of when to buy and when to sell. Though it is tough to figure out the rock bottom of the market, but gathering many samples of data and applying sums, averages, and anomaly functions upon that data can help determine what the market trends are. Holistically speaking, it is very critical to have visibility into data. Especially from the performance perspective, being able to monitor that data on a single pane of glass brings a lot of value to the table versus having disparate systems and siloed teams.
