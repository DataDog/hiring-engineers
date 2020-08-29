### Prerequisites - Setting up the Environment

My Datadog environment setup includes an agent install on my laptop Windows OS and a Ubuntu Linux VM via Vagrant. The setup directions mention that any OS can be used, but having never worked with Vagrant before, I didn't want to pass up an opportunity to challenge myself and learn something new. It was certainly also a backup in case I really did run into dependency issues--best to be prepared!

Upon downloading the Datadog Agent on my localhost, I'm now able to browse to http://127.0.0.1:5002/ where I can view my connection as well as other agent info. This UI also provides the ability to restart the agent service. Neat!

![Agent Manager](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager.PNG "Agent Manager")

Here's my agent manager, up and running. 

### Collecting Metrics
#### Tagging

Agent configuration occurs in the datadog.yaml file, which is my first stop in the tagging task. On a Windows OS, the file's located in C:\ProgramData\Datadog, and /etc/datadog-agent/ in a Linux environment. 

Within datadog.yaml, I add a variety of tags under the tags section. 

![Windows datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/windows_tags_config.PNG "Windows datadog.yaml")
![Linux datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/ubuntu_tags_config.PNG "Linux datadog.yaml")

Once the tags are added, the file gets saved, the agent service is restarted, and after 15-30 minutes, the newly-added tags appear in the host info section within the host map. 

![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_windows_tags.PNG "Windows Host Map - Tags")
![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_vagrant_tags.PNG "Vagrant Host Map - Tags")

#### Database Install and Integration

I utilized PostgreSQL for this portion of the exercise and started the database integration process by creating a dummy Datadog database. This was followed by the creation of the datadog user. 

Note that in the user creation screenshot below, the 1234 password for the user is for show only. In a live Production environment, 1234 would be the last password you'd want to use. Highly unsecure. 0/10--would not recommend. 

![SQL Datadog User Creation](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/datadog_sql_user_creation.PNG "Datadog DB User Creation")

Once the user's created, we enable the postgres.d configuration file in C:\ProgramData\Datadog\conf.d\postgres.d. The config file is filled out accordingly, and the agent gets restarted for the integration changes to take effect. 

![Postgresql Config Enable](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgres_config_updated.PNG "Postgres.d Configuration")

Following the enabling of the Postgres integration, I'm now able to pull metrics related to postgresql. To check how the integration allows Datadog to interact with Postgres, I pull up the db.count Postgres metric graph. An initial look shows I have one database, and upon creating another Test database, the graph count jumps to two. Configurations within Postgres are monitored and mapped in Datadog.

![Postgresql Metrics](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgresql_metrics.PNG "Postgres Metrics")

#### Custom Agent Check

Setting up a custom agent check begins with the creation of a configuration file in C:\ProgramData\Datadog\conf.d and a check file in C:\ProgramData\Datadog\checks.d. To ensure a proper setup, the names of both files must match, and in our case, we're naming both "my_metric".  

There are a number of different functions or metric types that can be used for custom agent checks. Different functions/metric types result in different graphing capabilities and ultimately different displays. 

For my custom metric, I'm using the gauge function, which takes a value from a specific time interval and then continuously does so for each time interval after. This seemed to be the most appropriate type since we're looking to include a random value between 0 and 1000 in our check.

![Custom Agent Check](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/custom_check_code.PNG "Custom Agent Check")

### Visualizing Data

### Monitoring Data

### Collecting APM Data

### Final Question
