Prerequisites:  Setup the environment

I set up the originally set up a vagrant environment blindly using the defaults given in the link. These defaults provide Ubuntu 12.04. I didn't really run into any issues until I tried to configure the Collecting APM Data Section. This is when I started running into problems. I tried creating another image of 12.04 thinking that I poked around too much on the first image and may have caused a configuration issue. But I ran into the same issue of not being able to download the prerequisites to configure the software.

I then stopped using vagrant all together and used my Ubuntu 16.04 image that already had MySQL installed and installed the Datadog agent on that. Installation of the agent was super easy. I was able to download the prerequisites for Collecting APM Data Section. However, I was not able to get the given Flask application to execute properly. I was however able to run some test trigger successfully.

Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
I added a tag in the /etc/datadog-agent/datadog.yaml file.
            tags: my_datadog_yaml_tag:jon
<p align="center"><img src="host_map_tags.png" width="500" ></img></p>
In order for these tags to be active, the process_config: element must be enabled by also placing the following statement in the  /etc/datadog-agent/datadog.yaml file.

            process_config:
             enabled: true

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MySql database and the agent onto the image. Configuration of the agent was very simple using the following commands:

            sudo mysql -u root -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'p_KOOye63XjZjSBRMwr2s2c8';"
            sudo mysql  -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
            sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
            sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

Running the following commands validated the the configuration was successful. AS you can see from the screen shot, both commands display "MySQL user - OK"

            mysql -u datadog --password='p_KOOye63XjZjSBRMwr2s2c8' -e "show status" | \
            grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
            echo -e "\033[0;31mCannot connect to MySQL\033[0m"


            mysql -u datadog --password='p_KOOye63XjZjSBRMwr2s2c8' -e "show slave status" && \
            echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
            echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

<p align="center"><img src="integration_validation.png" width="500" ></img></p>
-------
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?


As you can see from the two screenshots, the original configuration gave an interval of approximately 20 seconds. Where the 2 time stamps in each of the images show the consecutive time intervals as being approximately 45 (40) seconds.

<p align="center"><img src="my_metric1.png" width="500" ></img></p>
By simply changing the configuration file to the following, I was able to change the collection interval to 45 seconds.
<p align="center"><img src="my_metric2.png" width="500" ></img></p>
My intial configuation file for the agent was the following

conf.d/my_metric.yaml:
---------------------

        init_config:

        instances:

---------------------


checks.d/my_metric.py:
---------------------
        import random
        from checks import AgentCheck
        class MyMetric(AgentCheck):
            def check(self, instance):
                self.gauge('my_jon_metric', random.randint(0,1001))


conf.d/my_metric.yaml:  Version 2 - 45 second intervals
---------------------
        init_config:

          instances:
                - server: localhost
                  min_collection_interval: 45
---------------------

Changing the collection interval is also possible by using the python API, however, I think a best practice would be to change configuration files instead of python code. By taking this approach, I also completed the "Bonus Question"

Monitoring Data

I created a Metric Monitor that watches the average of my custom metric (my_jon_metric) and will alert if it’s above the following values over the past 5 minutes: (code from above is included here for convenient reference)
---------------------
          import random
          from checks import AgentCheck
          class HelloCheck(AgentCheck):
              def check(self, instance):
                  self.gauge('my_jon_metric', random.randint(0,1001))
---------------------
Here are the emails that were generated for Aler, Warning and No Data.

<p align="center"><img src="Alert_monitor.png" width="500" ></img></p>
<p align="center"><img src="Warning_monitor.png" width="500" ></img></p>
<p align="center"><img src="NoData_monitor.png" width="500" ></img></p>

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.

Here are the screenshots of the configuration in the Datadog Web Site.
<p align="center"><img src="weekdaydowntime.png" width="500" ></img></p>
<p align="center"><img src="weekenddowntime.png" width="500" ></img></p>

Here are the screenshots of the emails I received cinfirming the schedule the downtime.
<p align="center"><img src="weekenddowntimeemail1.png" width="500" ></img></p>
<p align="center"><img src="weekenddowntimeemail2.png" width="500" ></img></p>
