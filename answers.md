Your answers to the questions go here.

# My solution to the Solutions Engineer questions
## - Hetansh Madhani

# My solution to the Solutions Engineer questions
## - Hetansh Madhani

### Prerequisites - Setup the environment:
I used Ubunut 18.04 as my operating system which I started in VM VirtualBox

I used the command given on the Datadog Installation Docs:
```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Where I used the API key I found after creating the account and replaced it in the command above at *YOUR_API_KEY*
- - - -
### Collecting Metrics:
#### Question: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
#### Adding tags in the agent config file.

I needed to edit the _datadog.yaml_ file to add the tags. Here is the snapshot of the file after editing.
![Tags Configured File](https://s3.amazonaws.com/solutions-engineer-photos/tag_file.png)

Here is the screenshot of my host and its tags on the Host Map page in Datadog Agent reflecting the tags I added in the config file.
![Tags Reflected in Agent](https://s3.amazonaws.com/solutions-engineer-photos/tags_agent.png)
- - - -
#### Question: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

For this task I decided to go with PostgreSQL. I installed PostgreSQL on my ubuntu machine using the following command:
```
sudo apt install postgresql postgresql-contrib
```
I followed the integration steps found in the agent as well the Datadog Support Documents on the official Website
https://docs.datadoghq.com/integrations/postgres/

I had to creat edit the *__postgres.yaml__*  file in *__conf.d/postgres.d/__* to make the agent collect PostgreSQL metrics and logs
![PostgreSQL Configured File](https://s3.amazonaws.com/solutions-engineer-photos/postgres_yaml.png)

I could see the integration was successful in the agent. 
![PostgreSQL Success in Intergrations](https://s3.amazonaws.com/solutions-engineer-photos/post_success.png)
![PostgreSQL Showed in Host](https://s3.amazonaws.com/solutions-engineer-photos/postgres_agent.png)
- - - -
#### Question: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
To write and create a custom Agent check I referred the following guide on the Official Docs:
https://docs.datadoghq.com/developers/agent_checks/

I had to create 2 files:
   - *__my_metric.yaml__* in *___conf.d/__* for configuring the agent check 
   - *__my_metric.py__* in *___checks.d/__* for writing the what the agent check is suppose to do

*__my_metric.py__* is as shown:

![Custom Agent Check Metric File](https://s3.amazonaws.com/solutions-engineer-photos/check_py.png)

*__my_metric.yaml__* is as shown to include the 45 sec time interval:

We do that by adding ``` -min_collection_interval: 45 ```

![Custom Agent Check Configuration File](https://s3.amazonaws.com/solutions-engineer-photos/check_yaml.png)

We can check that the agent is posting once every 45 seconds from referring the logs:

![Custom Agent Check Logs](https://s3.amazonaws.com/solutions-engineer-photos/check_log.png)
- - - -
#### Bonus Question Can you change the collection interval without modifying the Python check file you created?

I dont think so. (More research required)

### Visualizing Data: 
#### Question: Utilize the Datadog API to create a Timeboard
Here is my code to create the timeboard as asked
```
from datadog import initialize, api

options = {
    'api_key': '412d911e8166a2a1488c6fc8206b51cc',
    'app_key': 'aff723d2f7496c25a98ef3ca13d0cf342533e462'
}

initialize(**options)

title = "My Solutions Engineer Timeboard"
description = "Timeboard for solutions engineer task"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Hetansh-Ubuntu-VirtualBox}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric average over host: Hetansh-Ubuntu-VirtualBox"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.commits{*}, 'basic',2)"}
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL Commits"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric rollup visualization with time 1hr"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
resp = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

This created the timeboard with timeframe as 5 mins as shown in the image: 

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/timeboard.png)

To see the roll up function of 1hr applied to my_metric I changed the timeframe to past 4 hrs to see 4 values of each hour as:

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/roll_up.png)

#### Question: Take a snapshot of this graph and use the @ notation to send it to yourself.

Sending the graph to myself and also getting notified on email: 

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/atonation.png)
![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/events.png)
![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/email_anot.png)

#### Bonus Question: What is the Anomaly graph displaying?
The metrics are variable and it keeps on changing everytime. Figuring out what change, or what value of a metrics is abormal
or should trigger a alert is a tough task. Anomaly graph shows us the expected behavior of that particular value based on the historic
values of that metrics. It takes into account the past data corresponding to that day, time of day, etc. to give a gray band which covers
the range of the metric value expected to be normal. Anything outside the grey band is considered not normal.