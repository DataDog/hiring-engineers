## Prerequisites - Setup the environment
I followed the Vagrant setup documentation and successfully installed the VM. To install the Datadog Agent, I followed the instructions in the GUI by running the command below in my terminal: 

```
DD_API_KEY=4f03487948708ff3a0d41e3c69bd5b9a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"
```

Once this step was complete, I stopped the agent and launched the GUI by using the following commands: 

```
datadog-agent stop
datadog-agent start
datadog-agent launch-gui
```
![agent reporting metrics](/img/agent_report_metrics.png) 


#### Documentation I used to complete this section:
[Vagrant Setup Documentation](https://www.vagrantup.com/intro/getting-started/project_setup.html)  
[Datadog Overview](https://www.youtube.com/watch?v=mpuVItJSFMc)



## Collecting Metrics:
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

   I added the following tags: `env: production, and role:database` in the `datadog.yaml` config file which can be found in `opt/datadog-agent/etc/`. I inserted the tags with the `tags:` key in the `datadog.yaml` file. After adding the tags I restarted the Agent.

   ![Host Map page showing Tags](/img/hostmap_tag.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

   I am most familiar with MySQL so that's what I used for this challenge. It is already installed on my machine. 
   
   First, I created a database for the Agent by running the following query in MySQL: `CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'my_password';`. Then in order to verify that the user was created successfully I ran the following command: 

   ```
   mysql -u datadog --password='my_password' -e "show status" | \
   grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
   echo -e "\033[0;31mCannot connect to MySQL\033[0m"
   mysql -u datadog --password='my_password' -e "show slave status" && \
   echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
   echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
   ``` 

   Then, I edited the `conf.yaml` file in the `conf.d/mysql.d` directory in order to connect the Agent to my local MySQL server. I added the following code to the file: 

   ```
   instances: 
      - server: 127.0.0.1
        user: datadog
        pass: your_password_in_string
        port: 3306
        options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: true
          schema_size_metrics: false
          disable_innodb_metrics: false
   ```

   After these steps were complete, I restarted the agent. In the app, I confirmed that my integration was successful. Additionally, in the terminal I ran the check `datadog-agent check mysql` and confirmed the integration was successful.

   ![MySQL Integration](/img/mysql_integration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

   To create a new custom agent, I created a new check which I placed in `/etc/datadog-agent/checks.d/`. Then I inserted the following code in the file `my_metric.py`: 

   ```
    from checks import AgentCheck
    from random import randint

    class MetricCheck(AgentCheck):
      def check(self, instance):
        randomInt = randint(0, 1000)
        self.gauge('my_metric',  randomInt)
   ```

   After this step, I updated the file`conf.yaml` which is located in the ```/etc/datadog-agent/conf.d/mysql.d/``` directory

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

  In order to accomplish this, I updated the `my_metric.yaml` file, by updating the collection interval to 45. 

   ![45 second Collection Interval](/img/collection_interval.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

   Yes, I modified the collection interval in the `/etc/datadog-agent/conf.d/my_metric.d/conf.yaml` file that I created. I added `min_collection_interval: 45` to the instances section in order to achieve this collection interval. 


#### Documentation I used to complete this section: 
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
   
   Of the options in the API documentation, I'm most comfortable in the terminal so I used Curl. first I installed coreutils by using the following command: `brew install coreutils`. I generated a new app key in the settings section of the DataDog app found here: https://app.datadoghq.com/account/settings#api. 

  In order to add multiple graphs to the timeboard, I inserted multiple objects into the graph array. The issue I ran into was with escaping the quotes around `'basic'`. Once I determined how to do this, the script ran with no issues. The final timeboard can be found [here](https://app.datadoghq.com/dash/833933/my-timeboard-final?live=true&page=0&is_auto=false&from_ts=1528859389405&to_ts=1528862989405&tile_size=m)



```
api_key=4f03487948708ff3a0d41e3c69bd5b9a
app_key=43c5f29e91f2b86eb9db8cab1e7132a384f0c305

curl -X POST -H "Content-type: applicaiton/json" \
-d '{
  "title": "My Timeboard Final v1", 
  "description": "A New Timeboard with Metric Information",
  "graphs" : 
  [
    {
      "title": "my_metric scoped over host",
      "definition": {
        "events": [],
        "requests": [
          {"q": "avg:my_metric{host:nicholesvibrantlife}"}
        ]
      },
      "viz": "timeseries"

    },
    {
      "title": "Mysql Collection Anomallies",
      "definition": {
        "events": [],
        "requests": [
          {"q": "anomalies(avg:my_metric{host:nicholesvibrantlife}, \"basic\", 3)"}
        ]
      }, 
      "viz": "timeseries"
    },
    {
      "title": "my_metric w/rollup sum of points over an hour",
      "definition": {
        "events": [],
        "requests": [
          {"q": "avg:my_metric{host:nicholesvibrantlife}.rollup(\"sum\", 3600)"}
        ]
      }
    }
  ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

```

Once this is created, access the Dashboard from your Dashboard List in the UI.

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
   
   Issues: I could only determine how to create a 5 minute timeframe with screenboards so that is what I used to generate the 5 minute timeframe. 

   ![Screenboard timeframe set to past 5 minutes](/img/screenboard_timeframe_5.png)

   ![Screenboard timeframe annotated](/img/timeboard_annotated.png)


* Bonus Question
   The anomaly algorithmic feature is designed to identify when a metric is deviating from its past behavior. 

#### Documentation I used to complete this section:
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

   I created a mew monitor by going to the manage monitor page and clicking on New Monitor. You can easily customize your monitor on the page. This is where I set hte warning and alert threshold as well as requiring a notification if I received No Data for the query. 

   ![Alert Conditions](/img/alert_conditions.png)  

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

   The notification I received via email can be found in the screenshots below. The monitor can be found [here](https://app.datadoghq.com/monitors/5149754)

   ![Email configuration based on conditions](/img/email_config.png) 
   ![Email notification](/img/email_not_monitor.png)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* One that silences it from 7pm to 9am daily on M-F,
* And one that silences it all day on Sat-Sun.
* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification

   Muting the monitors overnight or on the weekend can be accomplished via the manage downtime section of the app. You can find this section by hovering over `Monitors` and selecting `Manage Downtown`. Once you fill in the required information, you will receive a confirmation email as well as an email at the start and end of the time you indicated 
  
   ![Silencing from 7pm - 9](/img/email_config_7-9.png | width=500)
   ![Silencing over the weekend](/img/email_config_weekend.png)
   ![Overnight Email](/img/overnight_email.png)  
   ![Weekend Email](/img/weekend_email.png)


#### Documentation I used to complete this section: 
[Monitoring docs](https://docs.datadoghq.com/monitors/)  



## Collecting APM Data
* Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

   First, I needed to install ddtrace. I did this by using pip and the folliwng commmadn: `pip install ddtrace`

   Then, I copied the provided script and placed it in the scripts/ directory. The flask app can be found [here](scripts/flaskapp.py)

   I ran into issues running `ddtrace-run python flaskapp.py`. These are the steps I followed to resolve the issue: 

     1. When I first ran dd-trace-run, I received the following error: 

       ```
       you must specify an API Key, either via a configuration file or the DD_API_KEY env var
       ```
       First, I believed the issue was that the trace-agent could not find access to the api key so I changed the `datadog.yaml` file from `api_key: 4f03487948708ff3a0d41e3c69bd5b9a` to `DD_API_KEY`. This did not resolve the error. 

     2. Next, I decided to give the Development configuration a try. I installed Go, then downloaded the latest source by running: `go get -u github.com/DataDog/datadog-trace-agent/...`. Then, I added a $GOPATH/bin to my bash_profile. Finally, I entered the following code into my terminal. 

     ```
     cd $GOPATH/src/github.com/DataDog/datadog-trace-agent
     make install
     ```

     When I entered `trace-agent --config /opt/datadog-agent/etc/datadog.yaml` the trace agent began to run on http://0.0.0.0:5050/. Next, I ran `ddtrace-run python flaskapp.py`. Then, I visited all of the routes on the flask app: /, /api/trace, /api/apm. After a few moments the app showed my traces on the APM->Traces section of the app. 

   [Link to Screenboard](https://p.datadoghq.com/sb/eebd8a387-76a7f7c7545fb03324f45304500a6080)  
   ![Dashboard](/img/Dashboard_apm_hostmap.png)

* Bonus Question

   A services is a set of processes that provide a feature set. An example would be a database like MySQL. A resource is a query to a service. A good example is the actual SQL of a database query like: `Select * from table_name LIMIT 5`


#### Documentation I used to complete this section:
[APM DOCS](https://docs.datadoghq.com/tracing/)  
[Setup APM in one minute](https://www.youtube.com/watch?v=faoR5M-BaSw)  
[Install Trace Agent on OSX](https://github.com/DataDog/datadog-trace-agent#run-on-osx)  
[Issues with installing DataDog Trace Agent](https://github.com/DataDog/datadog-trace-agent/issues/397)  
[Setting DD_API_KEY](https://github.com/DataDog/datadog-agent)  
[Tracing Visualization](https://docs.datadoghq.com/tracing/visualization/)  
[Datadog Trace Client](http://pypi.datadoghq.com/trace/docs/#get-started)  
[Tracing Setup](https://docs.datadoghq.com/tracing/setup/python/)  



## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

______

I'm an avid online shopper. I would be interested to track how many items are browsed before ultimately making the purchase. It would be interesting to track which items are browsed vs which items are purchased. 

I was inspired by the bathroom hack that the Datadog staff wrote about. I could see Datadog being used to monitor availability for mother's rooms in airports. Similar to the bathroom hack, the mother's rooms could have their locks monitored by a raspberry pi in order to show the status of whether or not they are in use. This would allow mother's to see which rooms are available throughout the airport so that they can quickly plan a route to the nearest room upon arrival. 



