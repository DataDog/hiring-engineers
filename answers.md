## Introdcution and Getting Started
Working on this exercise was definitely an insgihtful journey. This made me learn a lot about the Datadog solution itself and more importantly how the technology is working behind the scenes. The opensource nature of this product really makes Datadog a robust solution out in the market for infrastructure and application monitoring.
I decided to implement this exersice on my local environment (Windows 10). I did run into some dependency issues here and there but I was able to overcome them to successfully complete all the steps in the exercise. Also please notice that the screenshot links point to my own public github repo where I have uploaded them. Accessing those links should not be a problem. My findings are below:

## Collecting Metrics
The installation of the Datadog Agent itself was very straightforward. It is worth noting that the Agent itself has everything embedded inside of it. All the checks, integrations, python interpreter, etc. Yet the Agent is very lightweight.
Tiny snippet of the Datadog yaml file is below which shows the 3 tags I created. Followed by a screenshot of the Host Map in the Datadog UI.

*Tags in the Datado.yaml file*

    tags:
      - prac_env:cpu
      - prac_env:disk
      - prac_env:mem
    use_dogstatsd: true

*Datadog Host View Map Screenshot Link*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/HostMapView.png)

The tags reside in the Datadog's Agent yaml file. However, it is not necessary to make changes to the yaml file to change the configuration of the Agent. The changes can also be made by derectly launching the Datadog Agent Manager UI and navigating to the settings tab. The settings tab displays the yaml file and changes can be made directly there and saved. Once the changes are made, restart the Agent for the changes to take effect.

To integrate with a database, I went ahead with installing PostgreSQL on my local environment and configured the respective yaml file in the postgres.d folder within the Datadog Agent. To successfully integrate with Datadog, proper permissions to a user needed to be created. So I created a user 'datadog' with proper permissions. The configured yaml file is below:

*postgres.yaml*

    #postgres.yaml
    init_config:

    instances:
     - host: localhost
       port: 5432
       username: datadog
       password: Password1
       tags:
         - optional_tag
      
Once the configuration is set, I restarted the Datadog Agent. To view if Datadog was connected and collecting metrics from my postgres, I checked the 'Collector Status' from the Datadog Agent Manager. Find the screenshot below:

*Postgres Status Screenshot Link*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/PostgresStatus.png)

Creating custom agent check is actually a very nifty task. However, a multitude of integrations are offered OOTB but it is simple to write a check to montior something if it is not offered OOTB. Writing a custom python integration script to integrate it with Datadog just shows how powerful the opensource architecture is. It is very simple yet very powerful. A few things need to be kept in mind however while creating a custom agent check. For example, both .yaml and .py files must be of same name, otherwise Datadog will not pick up the configuration of the check. I created a separate folder in the conf.d folder called 'my_metric.d' where I stored the my_metric.yaml file. Next, I created the my_metric.py file to store it in the 'checks.d' folder embedded within the Datadog Agent folder. Below is the code for my_metric.yaml and my_metric.py to implement the custom agent check.

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
Datadog's Timeboard is a useful utility when it comes to visualizing data. The Timeboard provides many different options as to how you can customize your view of data. I have posted the screenshot link below of the Timeboard created via Datadog Timeboard API and the code is below as well.

*Timeboard via API Screenshot Link*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/CustomTimeboardviaAPI.png)

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

Also, I have posted the screenshot link below of the anomaly snapshot taken of the 5 mintue timeframe from the custom Timeboard graph.

*Anomaly Snapshot of 5 Mins Time Lapse Screenshot Link*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/PostgresAnomaly5minsGraph.png)

#### Bonus Question: What is the Anomaly graph displaying?
The Anomaly graph is displaying the Postgres max_connections metric and unusual spike that is outside of the standard deviation bounds.

## Monitoring Data
It is always good to know how overall infrastructure and applications are doing in terms of performance. Especially if they are critical to the business. Applications that generate a lot of revenue for an organization should be monitored very closely and of course the infrastructure the application is sitting on as well. Datadog's monitoring capabilties make it very simple and intuitive for anyone to start monitoring the metrics around the infrastructure and application. The monitor configurations also allow for users to schedule downtimes for alerts if the user does not want to be bothered off hours or notify on the spot if the data has gone missing for a few consecutive minutes. I have posted links for screenshots below:

*Screenshot link below of creating and configuring the monitors*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/CreatingMonitors.png)

*Screenshot link below of whenever a monitor is triggered and email notification is received*     
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MonitorTriggeredEmailNotification.png)

*Screenshot link below of monitor alert email notification when an alert is triggered for metric above 800. Provides the value of the sample and the host IP. Metric value is showing as 829.5*     
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MetricAlertEmailNotification.png)

#### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
*Screenshot of downtime scheduled in Datadog for 7pm - 9am on Mon-Fri*    
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/ScheduledDowntimeForOffHours.png)

*Screenshot of downtime scheduled in Datadog for all day weekends*      
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/ScheduledDowntimeForWeekends.png)

*Screenshot link below of downtime scheduled email notification recevied when downtime was scheduled*       
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/DowntimeScheduledEmailNotification.png)

*Screenshot link below of downtime started email notification received when downtime started*       
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/DowntimeStartedEmailNotification.png)

## Collecting APM Data
It is very critical to deliver an application into production with extreme quality. Organizations invest blood, money, and sweat to develop and deliver a robust and quality applications. Investing in good tools for functional testing and performance testing are very critical to delivering a quality application. But what about once the application is released into production? Is it not equally important, if not more, to keep monitoring the performance of that application once it is delivered in the hands of an end user? From my perspective, it is MORE important to monitor how the application is performing out in the real world. When an organization tests the application before release, they test the application with basic use cases assuming how the end user may react with the application. But the reality is, we cannot restrict the actions of end users and cannot limit them to using the application in a specific way, which is why it becomes very critical to monitor the application and its performance after it is in production.
With Datadog's APM solution and its opensource nature, it becomes very flexible to instrument the application with Datadog's tracer. Datadog APM supports a number of frameworks and technologies OOTB. Datadog offers a couple of neat ways to instrument the application - automatic instrumention or manual instrumentation. Below is a Flask application instrumented manually with Datadog's tracer followed by a public URL of Datadog's Dashboard with both APM and Infrastructure metrics.

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
    
Link below of the public URL of my Datadog Dashboard. The application will need to be executed via cmd or terminal and then navigate to 0.0.0.0:5050 to input requests for data to populate in the Timeboard and Dashboard. I have also included screenshot links below of the APM Timeboard, custom dashboard, APM flame graphs. Please view the screenshot links below:

*Datadog Dashboard Public URL*
(https://p.datadoghq.com/sb/5a3d8d1c0-861d08d9512c0fb276dfc7dc625ee24e)

*My Flask App Flame Graph Screenshot Link*     
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/APMFlameGraph.png)

*My Flask App In Datadog Screenshot Link*      
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyFlaskAppInDatadog.png)

*My Flask App Service Screenshot Link*       
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyFlaskAppService.png)

*My Custom Screenboard With APM and Infrastructure Metrics Screenshot Link*      
(https://github.com/shahmoa/DD-Challenge-Exercise/blob/master/MyCustomScreenboard.png)

#### Bonus Question: What is the difference between a Service and a Resource?
In the context of APM, a service is a set of processes or software that provide a set of functionality. A resource is a subset of a service or a particular action catered to that service. service can have many individual resources. For example, www.datadog.com is whole service provided to a user. When a user logs into their account by going to www.datadog.com/login, that 'login' functionality serves as an endpoint resource to that service.

## Final Question - Is there anything creative you would use Datadog for?
Given the flexibility, robustness, and opensource nature of Datadog, I can think of many creative ways Datadog can be applied to real life scenarios. A good one would be monitor very obvious correction that is happening in the market. Stocks are dropping because of uncertainty in the elections, the tarrifs, and othe factors played. The point being, it would be really neat to monitor the trends an analysis of the market ups and downs to make educated decisions of when to buy and when to sell. Though it is tough to figure out the rock bottom of the market, but gathering many samples of data and applying sums, averages, and anomaly functions upon that data can help determine what the market trends are. Holistically speaking, it is very critical to have visibility into data. Especially from the performance perspective, being able to monitor that data with a single pane of glass view bring a lot of value to the table versus having disparate systems and siloed teams.
