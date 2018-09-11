# Solutions Engineer Exercise

## Setup
For this open source exercise I'm running Ubuntu 16.04 on my device. Before installing the agent, I read through the documentation located at the bottom of the assignment in order to gain an understanding of the Datadog agent.  

Download the Datadog Agent in terminal.
```
DD_API_KEY=f3a6ab39d4e712b846b54ad0ccaa2083 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/agent_ok.png" />


## Collecting Metrics
Tagging gives the user a method of aggregating data across a number of hosts. This is useful because users can then compare and observe how metrics behave across a number of hosts or collection of systems. 
navigate to Datadog directory

```
cd /etc/datadog-agent
```
Open Datadog.yaml:
```
sudo vim Datadog.yaml
```
Configure your .yaml file and change the tags to your preference. These are my tags:
(insert tag.png photo)

Restart the agent:
```
sudo service datadog-agent restart
```
Navigate to Host Map page in Data dog. Reload the page if your new tags do not appear.
Here is my Host Page map for reference.
(insert Host_page.png)

### Install a database. For this part, I went ahead with MySQL.
to install MySQL, run:
```
sudo apt-get update
sudo apt-get install mysql-server
```
After installation, configure it with Datadog. 
First I create a datadog user with replication rights in my MySQL server. Then I add the full metrics. 
Next I edit conf.d/mysql.yaml.
(insert mysql_yaml.png)

To see that MySQL is sucessfully running its metrics, restart the Datadog agent then type, 
```
sudo datadog-agent status
```
This shows that my metric is running successfully:
(insert check_mysql.png)
MySQL is shown to be configured and can be seen on the dashboard:
(insert mysql_dashboard.png)

### Adding a custom Agent check
Again, I spent alot of time reading through the agent_check documentation. From the guidelines and example .py and .yaml files in that document, I created two files, one python file named my_metric.py which was placed in directory /etc/datadog-agent/checks.d/my_metric.py. The other files, my_metric.yaml was placed in directory /etc/datadog-agent/conf.d/my_metric.yaml.
My my_metric.py:
(inset my_metric_py.png)

My my_metric.yaml
(insert my_metric_yaml.png)

Also remember to restart the Agent so that the metrics can be updated. 

We are now creating random numbers between 0-1000 as seen on my dashboard.
(insert my_metric_dash)

To change my checks collection interval so that it only submits once every 45 seconds is done by changing my_metric.yaml. Now according to the checks_agent documentation, the ```min_collection_interval``` is defaulted to 0 seconds when it is not added. 
my_metric.yaml now looks like this with a collection interval time of 45 seconds:
(insert interval_my_metric.png)
(insert collection_metric.png

*Can you change the collection interval without modifying the Python check file you created?*
Yes, I can change the interval by editing my my_metric.yaml file and setting ```min_collection_interval``` to 45. 




