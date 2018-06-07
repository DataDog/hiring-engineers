## Prerequisites - Setup the environment
* I decided to install vagrant to avoid any dependency issues. 

   ![agent reporting metrics](/img/agent_report_metrics.png) 

##### Documentation I used to complete this section:
_______________  
[Vagrant Setup Documentation](https://www.vagrantup.com/intro/getting-started/project_setup.html)  
[Datadog Overview](https://www.youtube.com/watch?v=mpuVItJSFMc)  

## Collecting Metrics:
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

   ![Host Map page showing Tags](/img/hostmap_tag.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

   I use MySQL so that's what I used for this challenge. 
   ![MySQL Integration](/img/mysql_integration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

   ![Custom Agent Check with Random Value](/img/custom_agent_randomint.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

   ![45 second Collection Interval](/img/collection_interval.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

   Yes, I modified the collection interval in the yaml file.


##### Documentation I used to complete this section:
________  
[Datadog Doc - How to use Tags](https://docs.datadoghq.com/getting_started/tagging/using_tags/)  
[Datadog Doc - How to assign Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/)  
[Datadog Doc - MySQL Integration ](https://docs.datadoghq.com/integrations/mysql/)  
[APM in a minute](https://www.youtube.com/watch?v=faoR5M-BaSw)  
[Writing an Agent Check](https://docs.datadoghq.com/developers/agent_checks/)  
[Agent Commands](https://docs.datadoghq.com/agent/faq/agent-commands/)  
[Python - Random Int](https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9)  


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
   Did not Implement

```
api_key=4f03487948708ff3a0d41e3c69bd5b9a
app_key=43c5f29e91f2b86eb9db8cab1e7132a384f0c305

curl  -X POST -H "Content-type: application/json" \
-d '{
	  "query":"time_aggr(last_1h):anomalies(sum:my_metric{host:nicholesvibrantlife}, 'basic', 3, direction='above', alert_window='last_15m', interval=60)",
      "graphs" : [{
          "title": "My Metric Timeboard",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "sum:my_metric{host:nicholesvibrantlife}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "My Metric Timeboard",
      "description" : "A dashboard with memory info.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

   From the research I conducted, I could only find a way to show a 5 minute timeframe using screenboards. 

   ![Screenboard timeframe set to past 5 minutes](/img/screenboard_timeframe_5m.png)

   ![Screenboard timeframe set to past 5 minutes](/img/timeboard_annotated.png)

##### Documentation I used to complete this section:
________  
[Anomaly](https://docs.datadoghq.com/monitors/monitor_types/anomaly/)  
[Pretty Print in Terminal](https://stackoverflow.com/questions/26935353/pretty-print-python-dictionary-from-command-line)  
[Create Monitor](https://docs.datadoghq.com/api/?lang=bash#monitors)  
[Rollup](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1)  
[Timeboard Video](https://docs.datadoghq.com/videos/datadog101-3-dashboards/?wtime=40.5)  


## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

   ![Alert Conditions](/img/alert_conidtions.png)  

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

   ![Email configuration based on conditions](/img/email_config.png) 
   ![Email notification](/img/email_not_monitor.png)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* One that silences it from 7pm to 9am daily on M-F,
* And one that silences it all day on Sat-Sun.
* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification
  
   ![Silencing from 7pm - 9](/img/email_config_7-9.png) 
   ![Silencing from 7pm - 9](/img/email_config_weekend.png)



##### Documentation I used to complete this section:
________  
[Monitoring docs](https://docs.datadoghq.com/monitors/)  


## Collecting APM Data
* Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

   ![Link to Screenboard](https://p.datadoghq.com/sb/eebd8a387-be289566f95d4b06ee753f7a7f153634)
   ![Dashboard](/img/Dashboard_with_APM_and_Infrastructure_Metric.png)



##### Documentation I used to complete this section:
________  
[APM DOCS](https://docs.datadoghq.com/tracing/)  
[Setup APM in one minute](https://www.youtube.com/watch?v=faoR5M-BaSw)  
[Install Trace Agent on OSX](https://github.com/DataDog/datadog-trace-agent#run-on-osx)  
[Issues with installing DataDog Trace Agent](https://github.com/DataDog/datadog-trace-agent/issues/397)  
[Setting DD_API_KEY](https://github.com/DataDog/datadog-agent)  
[Tracing Visualization](https://docs.datadoghq.com/tracing/visualization/)  
[Datadog Trace Client](http://pypi.datadoghq.com/trace/docs/#get-started)  
[Tracing Setup](https://docs.datadoghq.com/tracing/setup/python/)  



