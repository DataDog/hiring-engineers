In this exercise, I'll cover:
- setting up a VM with Vagrant
- installing and configuring the Datadog Agent
- setting up the MySQL Intergration
- adding custom Datadog checks
- creating visualizations with the Datadog API
- setting up and managing Monitors
- setting up Datadog APM

Let's get started!


## Set up, Tagging, and Metrics

### Create a Vagrant VM and Install Datadog

To set up a Vagrant VM, follow their [getting started guide](https://www.vagrantup.com/intro/getting-started/). I suggest using one of their standard Ubuntu boxes like `hashicorp/precise64` or `ubuntu/trusty64`. Once your VM is up, log in to the VM and add the Datadog Agent with teh following commands.

```
vagrant ssh
sudo -s
apt-get update && sudo apt-get -y upgrade
#if your box does not come with curl installed
apt-get -y install curl 
DD_API_KEY=<YOUR_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Tags in Datadog allow you label and divide up your infrastructure into meaningful segments based on things like availability-zone, role, environment, etc. To add tags to your `datadog.yaml` with the following commands:

```
cd etc/datadog-agent

# If you try to edit the existing datadog.yaml file to add tags and find that  
#the tags you add are not reflected on your Datadog Host Map, you can delete and recreate the file.
#All information except your API key and the dd_url will still be available in the datadog.yaml.example file.

rm datadog.yaml
touch datadog.yaml
echo -e "dd_url: https://app.datadoghq.com \napi_key: '<YOUR_API_KEY>' \ntags: YOUR_TAG1:VALUE1, YOUR_TAG2:VALUE2, YOUR_TAG3:VALUE3" >> datadog.yaml 
```

From here, you can log in to your Datadog app, navigate to Host Map under Infrastructure, click on your host, and see the tags you added listed under "Datadog". For further reading on agent setup and configuration, check out the [Agent](https://docs.datadoghq.com/agent/) section of the Datadog docs


![dd_tags](https://user-images.githubusercontent.com/8127456/37919248-387723f8-30d8-11e8-90cd-a15e9ee2bfd3.png)

## Setting up the MySQL integration

To set up the MySQL integration, install MySQL on your machine. The commands below can be used to install MySQL on an Ubuntu box.

```
apt-get install mysql-server 
# create a root password when prompted
mysql_secure_installation
#no need to change your passord, but answer yes to all other options
mysql -u root -p
```

From here you can set up the Datadog user and password as detailed in the [MySQL Integration docs](https://docs.datadoghq.com/integrations/mysql/). The steps are below

```
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
# to check that the performance_schema table exists
mysql> show databases like 'performance_schema';
#to grant priviledges on the performance schema table
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost'; 
```

To check that all permissions are set correctly, exit MySQL and run the following command, with your password filled in:

```
mysql -u datadog --password='<UNIQUEPASSWORD>' -e "show status" | grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql -u datadog --password='<UNIQUEPASSWORD>' -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
```

Next add a `mysql.yaml` file to the `conf.d` directory. The basic contents for the file are below, but you can see more options in the Datadog [`mysql.yaml.example` file](https://github.com/Datadog/integrations-core/blob/master/mysql/conf.yaml.example):

```
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: <UNIQUEPASSWORD>
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

Lastly, restart your Datadog agent and check to make sure you have enabled MySQL in the Integrations sections of the Datadog web UI.

![screen shot 2018-03-27 at 9 59 03 am](https://user-images.githubusercontent.com/8127456/37982769-574f9408-31a6-11e8-9b60-6c582e4ed065.png)

## Adding Checks

Two files are required to add a custom check to your Datadog agent:
- A Python file that contains the check method in the `checks.d` directory.
- A YAML configuration file in the `conf.d` directory

Both files must have the same name, the name of the metric you are measuring. To add a check that generates a random number between 0 and 1000 called "my_metric", create the respective `checks.d/my_metric.py` and `conf.d/my_metric.yaml` files.

`my_metric.py`

```
from checks import AgentCheck
import random

class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

`my_metric.yaml`

```
init_config:
  min_collection_interval: 45

instances:
  [{}]
```

For further reading on custom checks, head over to the [Agent Checks](https://docs.datadoghq.com/agent/agent_checks/) section of the Datadog Docs.

**Bonus Answer:**

To adjust this check so that it is sent at intervals of at least 45 seconds, you can either edit the python file to include a sleep interval of 45 seconds or add `min_collection_interval: 45` to the `my_metric.yaml` file, under `init_config:`. Note: This does not mean that the metric will be collected every 45 seconds, but that it will be collected at an interval no shorter than every 45 seconds. For more information on this distinction, read the [configuration section](https://docs.datadoghq.com/agent/agent_checks/#configuration) of the Datadog [Agent checks docs](https://docs.datadoghq.com/agent/agent_checks).

Here are two metrics that use the same python function in their `.py` file, but have different `min_collection_interval` values set in their `.yaml` files.

![screen shot 2018-03-27 at 2 30 21 pm](https://user-images.githubusercontent.com/8127456/37996124-7d356a7e-31cb-11e8-98ca-b6cf1b6dd25d.png)


## Visualization

### Creating Timeboards with the API

Datadog has an [easy to use API](https://docs.datadoghq.com/api/) for doing all kinds of tasks that developers and devops engineers need to automate. Creating timeboards is a task that could become time consuming with you had to do it by hand every time your team makes changes to your infrastructure. Fortunately, creating timeboards is a straight forward task that you can easily template with the Datadog API.

This example script creates a timeboard that contains graphs with:
- The custom metric from the last section scoped over a single host.
- Connections to the MySQL database from the last section, with the anomaly function applied.
- The custom metric from above with the rollup function applied to sum up all the points for the past hour into one bucket

Here's the timeboard that script generates:
![timeboard](https://user-images.githubusercontent.com/8127456/38001426-8f15e5fa-31e1-11e8-8157-feb186d18578.png)

By clicking and dragging over the last 5 minutes, we can zoom into that timeframe.
![5 minute view](https://user-images.githubusercontent.com/8127456/38001425-8efeed8c-31e1-11e8-8889-e811cd505642.png)

By clicking the camera icon, you can add a comment to a graph that appears in the Event Stream. Note that by @mentioning a user, you can notify them of comments or information that's relevant to them. Here I called out there aren't any values `avg:mysql.net.connections` that the `basic` anomaly functions registers as outside of the norm.
![event](https://user-images.githubusercontent.com/8127456/38001424-8ee6f5d8-31e1-11e8-827e-e05da83b92e3.png)

**Bonus Answer**
Datadog's anomaly algorithms use historical data from your metrics to determine if values are inside an expected range or if they are outside that range and therefore "anomalies."  Here is another time period that shows an anomaly in red. The gray area shows the range of potential values that are not considered anomalies.

![anomaly](https://user-images.githubusercontent.com/8127456/38001594-87d632c6-31e2-11e8-9853-d1428fadc9c7.png)

**Note**
This script uses a rollup to display the sum of `my_metric` each houe as bars on a timeseries graph. If I were to do this over, I would display it without a rollup and as a query value. The alternate code for that section would look like:

```
{
    "definition": {
        "events": [],
        "requests": [
           {"q": "avg:my_metric{*}",
            "aggregator": "sum"}
        ],
        "viz": "query_value"
    },
    "title": "Sum of My Metric over the last hour"
}]
```

## Monitoring

Datadog makes it easy to set [monitors](https://docs.datadoghq.com/monitors/) that warn or alert your team when any metric is above a tolerable threshold.

To set up a monitor, go to select New Monitor under Monitor in the menu. You can define a metric and scope it to a host or tag within your infrastructure. From there you can set custom alert conditions and set custom messages based on whether your metric has hit the "Warn" or "Alert" threshold, or if no data has been sent. Don't forget to mention the team or team member who should receive email notifications when the monitor is triggered.

Below is a sample configuration for a monitor on `my_metric`:
![monitor](https://user-images.githubusercontent.com/8127456/38002552-d0d75df6-31e7-11e8-95ca-c9fe14b75c29.png)

When the monitor is triggered, it sends a message like the one below to the relevant teams/team members mentioned in the custom message.
![montior email](https://user-images.githubusercontent.com/8127456/38003047-852ad466-31ea-11e8-9a11-258595407906.png)

**Bonus Answer:**
Monitors are great, but sometimes they can send noise that isn't useful or actionable. To control for this, you can configure scheduled downtimes for your monitors under the "Manage Downtime" tab.

![monitors](https://user-images.githubusercontent.com/8127456/38003315-ee6fd9f2-31eb-11e8-929e-0f04fda7ca2e.png)

To keep the team informed, Datadog can send notifications to alert team members to newly scheduled monitor downtimes:

![downtime notification](https://user-images.githubusercontent.com/8127456/38003434-5c06e032-31ec-11e8-96ea-8d2258e568e9.png)


## Collecting APM Data

Datadog allows you to view [metrics on applications](https://docs.datadoghq.com/tracing/) as well as on your infrastructure. This powerful tool allows you see how your apps and infrastructure are performing side by side in customized dashboards, like the one below:

![APM](https://user-images.githubusercontent.com/8127456/38146126-7302cfa0-3401-11e8-8fcc-4691741a1efd.png)


To set up Datadog's APM solution, make sure APM is enabled in the `datadog.yaml` on your host. Next, install the `ddtrace` library. For python you can simply `pip install ddtrace`. Finally instrument your application with a few lines of code, which you can see in this example Flask app.

To check out your APM metrics on their own, head to the APM section of Datadog and navigate to the "Services" or "Traces" pages. 

**Bonus Answer:**

In Datadog, a Service is a set of processes that do the same job, such as a web app or database. A Resource is particular action for a service. In the case of the simple Flask app above, the whole flask app is a service, and each route within it—'/', /api/apm', and '/api/trace'—is a single resource.


## Final Question

There are tons of cool ways to use Datadog. One non-traditional application that I think would be useful is installing the Datadog on the connected tools that people use for their outdoor hobbies. For example, there are commercially available spot trackers that hikers and bike packers take into the wilderness with them when they are going to be far away from cell service or internet access. These devices let you send a simple message via satellite a few times a day or at night to let loved ones know that you are OK, or to let them and emergency services know that you are in trouble. 

I am personally against using these for my outdoor adventures for a reason that I think Datadog could help address. Sometimes these devices run out of battery or have some other issue that prevents users from sending those messages. This means that instead of loved ones getting the relief of hearing "All's well!" they hear nothing, get worried, and start thinking of worst case she-got-eaten-by-a-bear scenarios.

If Datadog was installed and configured to check for metrics that often lead to or predict equipment failure on these devices, Datadog could send a quick message to the folks back home saying "I'm OK by my device is having some issues, you might not hear from me for a bit. Please don't worry!" If that feature came standard, I might start taking a tracker out with me.


## Final Thoughts

This was a great exercise that helped me get to know Datadog. I realize this is a lot to read, so thank you for getting this far and taking time out of your day to review my exercise!
