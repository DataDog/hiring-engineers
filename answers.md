# Prerequisites - Setup the Environment

I used the **macOS** environment to complete this exercise.

1- I created my account on https://www.datadoghq.com/
2- To install the **Agent** on my machine I chose the **Mac OS X** platform from the menu list because I'm using the macOS environment and copied this installation command (I removed the API KEY value from the command below to make sure that I don't expose it, and hid it using a black banner on the screenshot image below): 


`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<API KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"` 
![Agent Installation](/images/img1.png)

3- From here I was able to access the **Datadog Agent Manager** and check the Agent reporting metrics.

![Agent Status](/images/img2.png)

![Agent Logs](/images/img3.png)

# Collecting Metrics
## Adding Tags
I added tags in 2 ways by checking [Getting started with Tags](https://docs.datadoghq.com/getting_started/tagging/):
1- Manually using the configuation file where I search for the **tags** section and added 2 tags there and restarted the agent.

![Tags1](/images/img4.png)


2- Using the UI of the Host Map Page. I added 1 new tag

![Tags1](/images/img5.png)

## Database
### Database Local Installation
I decided to install and work with **MongoDB**.
I followed the [official mongoDB documentation](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) to install mongoDB community edition on my     local machine. I installed it with **brew** using these 2 commands: <br>
`brew tap mongodb/brew` <br>
`brew install mongodb-community@4.4` <br>
  
I started the MongoDB service using `brew services start mongodb-community@4.4` and to make sure that its running I used this command `brew services list`<br>
  
 ![MongoDB Started](/images/img6.png)
  
### Datadog and Database Integration
Now that I have MongoDB installed on my local machine, I need to install its corresponding Datadog Integration. I followed this [official Datadog document](https://docs.datadoghq.com/integrations/mongo/?tab=standalone) for the MongoDB integration.
I opened the **Mongo Shell** in the terminal using the command `mongo` and created a database with a read-only user.

```
#This creates a database named admin if it doesn't exist and starts using it
use admin 

# On MongoDB 3.x or higher, use the createUser command.
db.createUser({
  "user": "datadog",
  "pwd": "khalil22",
  "roles": [
    { role: "read", db: "admin" },
    { role: "clusterMonitor", db: "admin" },
    { role: "read", db: "local" }
  ]
})
```
![MongoDB Shell](/images/img9.png)


Now I need to configure the **Agent** running on the host. I edited the `mongo.d/conf.yaml` in the `conf.d` folder by adding the coressponding values and restarted the agent.

![MongoDB Config](/images/img7.png)

I was able to see that the mongoDB is succesfully integrated with Datadog. It was added to the Host Map and its status shows **OK**.

![MongoDB Status](/images/img12.png)

I added a **MongoDB Dashboard** by going to the **Dashboard** menu and installing it from there and since it's already integrated I was able to see the mongoDB metrics on the dashboard.

![MongoDB Dashboard](/images/img8.png)

## Cutsom Agent Check

I followed this official Datadog [documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) to create a custom agent check.
I created a file called `my_metric.py` in the `check.d` folder that is inisde `datadog-agent` directory. I took the example code of the documentation and modified it so it can generate a random number between [0,1000]. I used the `randint` function ot generate the random numbers.

```python
import random # to use the randint function

# the following try/except block will make the custom check compatible with any Agent version

try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```  
Next I created `my_metric.yaml` file in the `conf.d` directory. Here we need to make sure that the name of the python file matches exactly the name of the yaml file. So both need to be named `my_metric` in this case. I added the following lines the `my_metric.yaml` file:
```yaml
instances: [{}]
tags:
  - metric:my_metric
  - env:dev
```

Now that both the python file and the yaml configuration file of this custom metric are created, it's time to check if its working. I used this command to validate my custom metric `datadog-agent check my_metric` and it gave a succesful result.

![MongoDB Dashboard](/images/img11.png)




## Changing the Collection Interval
To change the collection interval, I reopened the `my_metric.yaml` configuration file and added a `min_collection_interval` parameter with the value `45` under `instances`, and restarted the agent.

```yaml
instances:
  - min_collection_interval: 45
tags:
  - metric:my_metric
  - env:dev
```

This time re-validate, I opened the Datadog Agent **Web UI**. I clicked on **Checks** from the menu list and then **Checks Summary**. I saw both `mongo` and `my_metric` working succefully.

![Checks](/images/img13.png)

**Bonus question**: Yes we can change the collection interval without modidying the python file created. Just like I did right now, I changed it directly from the YAML configuration file.

# Visualizing Data
## Using Datadog API to create Timeboard/Dashbaord
I used this official Datadog [API Reference](https://docs.datadoghq.com/api/latest/dashboards/) to create the dashboard. I created a Python file named `timeboard.py` that uses the Python code example from the API reference to generate the 3 visualizations:
- Custom Metric
- MongoDB Metric with the **anomalies** function. I saw the different  mongoDB's metrics in [this documentation](https://docs.datadoghq.com/integrations/mongo/?tab=standalone) and chose `mongodb.mem.resident`. This metric shows the amount of memory currently used by the database process.
- Custom Metric with the **rollup** fuction). 

To initialize the datadog client library I need my datadog `API_KEY` and `APPLICATION_KEY`. I already have my `API_KEY`  but to create the `APPLICATION_KEY` I clicked **Team** from the Datadog menu, then clicked on **Application Keys** and then **New Key** to generate my key with the name `demo-key`.

![Application Key](/images/img10.png)

I modified the script by looking at the **JSON** definition of the current visulization provided in the code example. I modified it to show my custom metric, and then added the 2 other visualizations with their correspnding functions.

```python
from datadog import initialize, api

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APPLICATION_KEY>'
}

initialize(**options)

title = 'Khalil\'s Dashboard'
widgets = [
    { #First Visualization: My Custom Metric scoped over my host Khalils-MBP
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:Khalils-MBP}'}],
        'title': 'my_metric timeboard'
    }
},

    { #Second Visualization: MongoDB's memory resident metric with the anomaly function applied
     'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mongodb.mem.resident{*}, 'basic', 2)"}],
        'title': 'MongoDB memory usage anomalies'
    }  
},

    { # Third Visualizaton: My Custom Metric with the rollup function applied 
      #to sum up all the points for the past hour into one bucket (1 hour = 3600 seconds)
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}],
        'title': 'my_metric rolling hour sum'   
    }
}]

layout_type = 'ordered'
description = 'A customized dashboard'
is_read_only = True
notify_list = ['khalilfaraj22@gmail.com']
template_variables = [{
    'name': 'Custom Timeboard',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'test'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)               
```



I already have Python installed so all I had to do was to install the Datadog client library that we are using inside the Python code. I installed the library using this command `pip3 install datadog` and then ran the script that generated my Dashboard with the visualizations.

## Accessing the Dashboard on Datadog

![Dashbaord List](/images/img14.png)

### Setting the timeframe to the past 5 minutes
I set the timeframe to the past 5 minutes, however there were no anomalies yet within this timeframe. (MongoDB's current memory used was stable at slighly less that 16 Mebibytes), and the rolling hour visualaization was still summing up the points since its the period defined is 1 hour.

![Dashbaord](/images/img15.png)


I waited a couple of hours and changed the timeframe to show me data within the last 4 hours. This time I started seeing anomalies and the rolling hour for `my_metric` started to show the data.

![Dashbaord After](/images/img16.png)

### Taking a Snapshot

![Snapshot](/images/img17.png)

![Snapshot Email](/images/img19.png)

**Bonus question**: Anomaly functions tells us if a metric has an abnormal behaviour. It uses past or previous data and process them to understand what values are normal for the metric that is being used. These values are represented in an overlaying gray band . In other words This band represents the expected values for the metric. For example if there was a fluctuation or a sudden spike of values for a metric but this fluctation is still in the gray band (in which the algorithm created using previous data), then this fluctuation is expected and is not an anomaly, but if the fluctuation was outside the range of the band then in this case, this is an anomaly.

## Monitoring Data

### Creating a New Metric
From the menu in Datadog, I clicked on **Monitors** then **Metric** in **Custom Monitors**.

![New Metric](/images/img18.png)

I added a name, selected my host `Khalil-MBP` and fill the required values for the **Alert Conditions**:

![Alert Conditions](/images/img20.png)

### Configuring the Monitor Message

Using the **Message Template Variable** I was able to write my Monitor Message:
```
{{#is_warning}}
**WARNING**: The average value of `my_metric` has been **slightly high** over the past **5 minutes**.
{{/is_warning}} 

{{#is_alert}}
**ALERT!** `my_metric` has been **high** over the past **5 minutes** at {{value}}  for {{host.name}} with IP {{host.ip}}.
{{/is_alert}}

{{#is_no_data}}
There has been **no** data for the  average value of `my_metric` over the past **10 minutes**.
{{/is_no_data}}
```
As requested the *value*, *host name* and *host ip* are defined in the **Alert** state.
Last part was to my email in the **Notify your team** section and clicked on **Save**

![Alert Config](/images/img21.png)

### Email Notifications Screenshots
#### Alert Status

![Alert Status](/images/img22.png)

#### Warning Status

![Warning Status](/images/img23.png)

#### Missing Data/

For this one I tested it using the **Test Notifications** Button

![Missing Data](/images/img24.png)

### Bonus

In the **Monitors** menu, I clicked on **Manage Downtime** and then **Schedule Downtime**. In here I chose the monitor that I created earlier, chose **recurring** and added the dates to make it silent from 7pm to 9am daily on M-F.

![Downtime1](/images/img25.png)

![Downtime1 Created](/images/img27.png)

![Downtime1 Email](/images/img26.png)

I repeated the same steps to create the second downtime that happens during the weekend. In the email notification you will see that I updated and rechanged the time. When I first created this downtime, once the day becomes Monday (12:00 am), the Monitor resumes which is something that we don't want because it's the middle of the night. So I changed it and add it 9 hours to it because the first downtime configuration starts at 9:00 am. So in this case, this Monitor will be silenced Saturday, Sunday and the first 9 hours of Monday (12:00am till 9:00am), and the first downtime created will proceed with the rest of the weekdays (7:00 pm till 9:00am).


![Downtime2 Created](/images/img28.png)

![Downtime2 Email](/images/img29.png)











































