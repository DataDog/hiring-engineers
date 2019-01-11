# Datadog Solutions Engineer Challenge - John Herbener
## Collecting Metrics
 -  #### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    -  In order to start collecting metrics from my host, I first had to install the agent on my Vagrant VM. The Datadog app makes it extremely easy with only requiring one command.
    - ```sh
        DD_API_KEY=<API KEY HERE> bash -c "(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
        ```
    - Once the agent was installed; I had to locate the configuration file for ubuntu at: /etc/datadog-agent/datadog.yaml.  Below is the configuration code to add host tags.

    - ```sh
        tags:
            - vm:ubuntu
        ```
    - After saving datadog.yaml, and restarting the agent, the host with the additional tags appear.

    - ![Host Tags](http://johnherbener.me/img/datadog/1.png)
    - Resources
        - https://docs.datadoghq.com/tagging/assigning_tags/?tab=go#configuration-files
        - https://youtu.be/xKIO1aWTWrk
        - https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6

 -  #### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    - Before installing an integration I had to install the database itself on my Vagrant VM. I chose MySQL because I have plenty of experience with it, and my hope was that this choice would make the process go a little smoother.
    - To install MySQL on Ubuntu it is simply two commands.
    - ```sh
        sudo apt-get update
        sudo apt-get install mysql-server
      ```
    - After installing MySQL, I had to create a database user for the datadog agent using the following command.
    - ```sh
        mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'password';
        ```
    - After verifying that the user is created I then had to grant the user certian permissions. Using the following commands from the docs.
    - ```sh
        mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
        mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
        mysql> ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
      ```
    - Once the DB is configured, it is time to configure the integration. The MySQL configuation file is located at: /datadog-agent/conf.d/mysql.d/conf.yaml.  Below is the code used to configure the MySQL integration.
    - ```sh
      init_config:
      instances:
        - server: 127.0.0.1
          user: datadog
          pass: 'password' # from the CREATE USER step earlier
          port: 3306 # e.g. 3306
          options:
              replication: 0
              galera_cluster: 1
              extra_status_metrics: true
              extra_innodb_metrics: true
              extra_performance_metrics: true
              schema_size_metrics: false
              disable_innodb_metrics: false
        ```
    - After configuring the MySQL integration, I restarted the Datadog Agent and MySQL metrics started to appear in the datadog application.
    - ![
](http://johnherbener.me/img/datadog/2.png)
    - Resources
        - https://docs.datadoghq.com/integrations/mysql/
        - https://youtu.be/xKIO1aWTWrk
        - https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/

 -  #### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    - After reading the section of the docs called, ' Writing a custom Agent check', it was clear to me that I needed two different files, but the docs mention that it is very important that the names be identical besides the extensions.
        - The first file is the YAML file.
        - > "The configuration file includes no real information but it is necessary to include a sequence called instances containing at least one mapping, that can be empty. "
        - ```sh
            instances: [{}]
            ```
        - The second file is the python file. It contains the logic.
        - ```sh
            import random
            from checks import AgentCheck

            class MyMetricCheck(AgentCheck):
                    def check(self, instance):
                            self.gauge('mymetric', random.randint(1, 1000) )
            ```
         - After the Custom Agent Check is complete we must verify that it is running. The docs gave me the command to do this.
	      - ```sh
	        sudo -u dd-agent -- datadog-agent check <check_name>
			 ```
		- ![
](http://johnherbener.me/img/datadog/3.png)
    - Resources
        - https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
        - https://youtu.be/xKIO1aWTWrk

 -  ####    Change your check's collection interval so that it only submits the metric once every 45 seconds.
    - After reading the doc's for the last section, I remembered reading about collection intervals, so I went back to that section and made sure I understood the question and saw that I did indeed read correctly.
	- > For Agent 6,  `min_collection_interval`  must be added at an instance level and is configured individually for each instance.
    - So mymetric.yaml must be updated with the code below.
     - ```sh
		init_config:  
		instances:  
			-  min_collection_interval:  45
		 ```
	- ![
](http://johnherbener.me/img/datadog/4.png)
    - Resources
        - https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6

  - **Bonus Question**  Can you change the collection interval without 	modifying the Python check file you created?
	  -  Yes. Change mymetric.yaml to the code below.
	  - ```sh
		init_config:  
		instances:  
			-  min_collection_interval:  45
		 ```


## Visualizing Data
 -  #### Utilize the Datadog API to create a Timeboard that contains:
    -  Your custom metric scoped over your host.  
	    - The first course of action I took was to head to the docs and see what I could find there. The docs provided me with an example python request to create a timeboard.
	    - ```python
			from datadog import initialize, api

			options = {
			    'api_key': '<YOUR_API_KEY>',
			    'app_key': '<YOUR_APP_KEY>'
			}

			initialize(**options)

			title = "My Timeboard"
			description = "An informative timeboard."
			graphs = [{
			    "definition": {
			        "events": [],
			        "requests": [
			            {"q": "avg:system.mem.free{*}"}
			        ],
			        "viz": "timeseries"
			    },
			    "title": "Average Memory Free"
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
			```
		- After adding my API and APP keys, all I had to do was change the metric that was being displayed to mymetric being scoped over my host. The following code completes this part of the question.
		- ```
		    "definition": {                        
		        "events": [],
		        "requests": [
		            {"q": "mymetric{host:ubuntu-xenial}"}
		        ],
		        "viz": "timeseries"
		    },
		    "title": "My metric"
		  ```
		 - ![
](http://johnherbener.me/img/datadog/5.png)
		 - Resources
		    - https://docs.datadoghq.com/api/?lang=python#timeboards
		    - https://youtu.be/U5RmKDmGZM4

	-   Any metric from the Integration on your Database with the anomaly function applied.
		- For this part of the exercise, I got stuck in a rabbit hole for a little bit, while investigating the Anomaly Monitor instead of the function itself. While looking at my MySQL graphs in that DataDog app, I picked one that seem to have a lot of movement because most the graphs were just straight lines. I ended up with mysql.performance.cpu_time as my metric.
		- After finding the correct documentation the implementation was pretty straight forward. I Just had to change the request from the previous answer.
		- ```
		    "definition": {                        
		        "events": [],
		        "requests": [
		            {"q": "anomalies(mql.performance.cpu_time{host:ubuntu-xenial}, 'basic', 2)"}
		        ],
		        "viz": "timeseries"
		    },
		    "title": "My MySQL metric"
		  ```
		- ![
](http://johnherbener.me/img/datadog/6.png)
		- Resources
			- https://docs.datadoghq.com/graphing/functions/algorithms/
		    - https://youtu.be/IGCcff2AcrQ

	-   Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
		- The documentation I read for the previous part of the exercise also provided me with the information I needed to complete this part.
		- > The function takes two parameters, method and time: `.rollup(method,time)`. The method can be sum/min/max/count/avg and time is in seconds.
		- All I needed to do was some simple math to find out how many seconds in a minute. 60x60 = 3600 seconds.
		- ```
		    "definition": {                        
		        "events": [],
		        "requests": [
		            {"q": "mymetric:{host:ubuntu-xenial}.rollup(sum, 3600)"}
		        ],
		        "viz": "timeseries"
		    },
		    "title": "My metric"
		  ```
		- Screenshot![
](http://johnherbener.me/img/datadog/7.png)
		- Resources
			- https://docs.datadoghq.com/graphing/functions/algorithms/
		    - https://youtu.be/IGCcff2AcrQ
		- ![
](http://johnherbener.me/img/datadog/8.png)

    - Set the Timeboard's timeframe to the past 5 minutes
	    - You can create custom timeframes by simply dragging your mouse across any graph on your dashboard. Stop when the correct amount of time is shown.
	    - ![
](http://johnherbener.me/img/datadog/9.png)
	- Take a snapshot of this graph and use the @ notation to send it to yourself.
		- ![
](http://johnherbener.me/img/datadog/10.png)
	- **Bonus Question**: What is the Anomaly graph displaying?  
		- > Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.
		- So basically the anomaly graph is displaying what the function thinks is going to happen according to historical data, account trends, seasonal day-of-week and time of day pattern. That is the grey section of the graph.

 ## Monitoring Data
 -  #### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
	 -   Warning threshold of 500
	 -  Alert threshold of 800
	 -   And also ensure that it will notify you if there is No Data for this query over the past 10m.
	 - ![
](http://johnherbener.me/img/datadog/11.png)
	- This is done completely by the Datadog UI and is self explanatory.
	 - Resources
		 - https://docs.datadoghq.com/monitors/monitor_types/metric/

- Please configure the monitor’s message so that it will:
	-   Send you an email whenever the monitor triggers.
		- This is simply done by tagging someone in step 5 of the monitor set up.
	-   Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
		- I completed this by utilizing message template variables. I used `{{#is_warning}}, {{#is_alert}} and {{#is_no_data}}.`
	-   Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
		- I completed this by utilizing message template variables. I used `{{host.name}}, {{host.ip}}, and {{value}}`.
   - ![
](http://johnherbener.me/img/datadog/16.png)
   	-   When this monitor sends you an email notification, take a screenshot of the email that it sends you.
	   	- ![
](http://johnherbener.me/img/datadog/19.png)
   - Resources
	   - https://docs.datadoghq.com/monitors/monitor_types/metric/
	   - https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning

- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
	-   One that silences it from 7pm to 9am daily on M-F,
	-   And one that silences it all day on Sat-Sun.
	-  Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
		- Everything is done in the UI and the screenshots so exactly how each downtime was created.
		- ![
](http://johnherbener.me/img/datadog/12.png)
		- ![
](http://johnherbener.me/img/datadog/13.png)
		- ![
](http://johnherbener.me/img/datadog/14.png)
		- Resources
			- https://docs.datadoghq.com/monitors/downtimes/

## Collecting APM Data
 -  #### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution.
	 - The very beginning of this section seemed to fly by, but soon I would hit a roadblock. After using the ddtrace command I simply didn't know what to do until I started reading the flask documentation and realized I what I needed to do.
	 - I also ran into the assume of naming the file flask.py and in that case it was trying to import flask from itself. After finally getting the dd-trace command to run, and reading through the flask documentation I realized I had to hit each of the endpoints defined in the flask app with a curl request.
	 - `example: curl 0.0.0.0:5050/api/trace`
	 -  After the requests were made the APM traces started show on the Datadog UI.
	 - ![
](http://johnherbener.me/img/datadog/17.png)
      - ![
](http://johnherbener.me/img/datadog/18.png)
	 - Resources
		 - https://docs.datadoghq.com/tracing/languages/python/
		 - http://pypi.datadoghq.com/trace/docs/
		 - https://stackoverflow.com/questions/14792605/python-flask-import-error
		 - http://flask.pocoo.org/docs/0.12/quickstart/
		 - https://unix.stackexchange.com/questions/148985/how-to-get-a-response-from-any-url
 -   **Bonus Question**: What is the difference between a Service and a Resource?
	 - > A service is a set of processes that do the same job
		 - -   A single  `webapp`  service and a single  `database`  service.
	 - > A Resource is a particular action for a service
		 -  While a more complex environment may break it out into 6 services:
			-   3 separate services:  `webapp`,  `admin`, and  `query`.
			-   3 separate external service:  `master-db`,  `replica-db`, and  `yelp-api`.
	 - Resources
		 - https://docs.datadoghq.com/tracing/visualization/

## Final Question
- Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
- Is there anything creative you would use Datadog for?
	- I would use Datadog to monitor my personal media server. My media server is running on a UNRAID(linux) install with a containerized approach. All of the applications running on the server are docker applications. So after  completing this challenge I may use Datadog to help optimize my media server for best performance. I think it would provide me with invaluable data.
