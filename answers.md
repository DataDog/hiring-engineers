# Mid-Market Engineer Application 

## Prerequisites- Set up the environment
#### Vagrant setup
I opted to follow the advice and completed the exercise using the suggested Ubuntu Vagrant VM setup.
![Alt text](https://i.imgur.com/CPJ4jAN.png "vagrant up")

Reference info:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

#### Datadog signup
I continued by signing up for trial online and using the one-step install command for agents. This completed the install for me seamlessly.

## Collecting Metrics
#### Adding tags
Tag was added in the /etc/datadog/datadog.yaml file as seen below:
![Alt text](https://i.imgur.com/hA9RElG.png "tags added .yaml")
The tags can also bee seen in the host online as seen here: 
![alt text](https://i.imgur.com/ozOXgdZ.png?1 "tags online")
Reference info: 
https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments

#### Installing mongodb and mongodb datadog agent
I followed the guide for setting up mongodb and it started successfully as seen below:
![alt text](https://i.imgur.com/B8Naffl.png "Mongodb started")

I created a user for the datadog agent and assigned permissions on the mongodb. I then configured this in the datadog mongodb config
```bash
sudo vim /etc/datadog-agent/conf.d/mongo.d/conf.yaml
```
![alt text](https://i.imgur.com/wevWaNi.png?1 "mongo datadog config")

We can then see this data in Metrics Explorer.
![alt text](https://i.imgur.com/E3Daw0w.png "Mongodb data")

Reference info:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
https://docs.datadoghq.com/integrations/mongo/?tab=standalone

#### Creating a custom Agent 

I created a bare bones config file containing just instances. 
```bash
sudo vim /etc/datadog-agent/conf.d/my_metric.yaml
```
Then I created a check file with same name my_metric.py and added a basic configuration as seen below. I imported random and used the random.randInt(1,1000) to get a random value between 1 and 1000.
```bash
sudo vim /etc/datadog-agent/checks.d/my_metric.yaml
```
![alt text](https://i.imgur.com/mbBokBU.png "Mongodb data")

The I tested using: 
```bash
sudo -u dd-agent -- datadog-agent check my_metric
```
Seeing the following result:
![alt text](https://i.imgur.com/S4xQz0Y.png "")

Reference info:
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

#### Change metrics to every 45 seconds 
 I edited the datadog-agent/conf.d/my_metric.yaml to add the interval: 
![alt text](https://i.imgur.com/Sb63Mul.png"")

This change can be seen happening on metrics Explorer here: 
![alt text](https://i.imgur.com/eBeu9Re.png"")

Reference info:
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

#### Bonus Question: Change it without editing python file?
This is done above it previous section by editing .yaml file.

## Visualizing Data

#### Code 

Here I created using the Datadog API using Python. Notes for this section:

 - API/App key got from website
 - I picked the "mongodb.network.bytesinps" as its movement allowed for some visualization of the anomalies prediction
 - 
The script is here below:

```python
from datadog import initialize, api
options = {
            'api_key': '***************',
            'app_key': '***************'
}

initialize(**options)
title = 'my_metric Visualization'
widgets = [{
            "definition": {
                 "title": "my_metric",
                 "type": "timeseries",
                 "requests": [
                       {"q": "avg:my_metric{*}"}
                 ]
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {"q": "anomalies(mongodb.network.bytesinps{*}, 'basic', 2)"}
                 ],
                "title": "Mongodb graph"
            }
        },
        {
            "definition": {
                "type": "query_value",
                "requests": [
                      {"q": "my_metric{*}.rollup(sum,3600)"}
                ],
             "title": "my_metric point over last hour"
            }
        }
]
layout_type = 'ordered'
is_read_only = True

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     is_read_only=is_read_only)
```

Reference info:
https://docs.datadoghq.com/api/latest/dashboard-lists/#get-a-dashboard-list
https://docs.datadoghq.com/dashboards/functions/rollup/#pagetitle

#### Visualization

Copy of dashboard over 5 minutes: Link: https://app.datadoghq.eu/dashboard/am3-7rw-56y/mymetric-visualization?from_ts=1621246974749&live=true&to_ts=1621247274749
![alt text](https://i.imgur.com/Ow3Cyh3.png "")

- We can see the slight grey tint on the Mongodb graph this shows us the predicted range for this metric. Anything outside this range would be considered an anomaly.
- My metric point over last hour is showing no data as there isn't an hour worth of data in a 5 minute view.

I was only able to send a snapshot for individual graphs and not a full dashboard:
![alt text](https://i.imgur.com/R8KFKHs.png "")

Here is the email I received: 
![alt text](https://i.imgur.com/AqDPneM.png "")

Reference info:
https://docs.datadoghq.com/dashboards/sharing/

#### Bonus Questions: Anomaly 
The anomaly range is showing the predicted range of the metric. This is in a grey tint.
Any value outside this range is considered and anomaly. This will be highlighted in red and make it obvious to a viewer there is an issue / something to investigate.

Reference info:
https://docs.datadoghq.com/api/latest/dashboard-lists/#get-a-dashboard-list
https://docs.datadoghq.com/dashboards/functions/algorithms/#anomalies 

## Monitoring Data

I completed the configuration on alert on the values and to send emails based on severity as specified and a lot of this configuration is visual so I will put a series of screenshots here:
![alt text](https://i.imgur.com/xeZ06WW.png "")
![alt text](https://i.imgur.com/tDWIgRn.png"")
Sample email: 
![alt text](https://i.imgur.com/AhZus5P.png "")

#### Bonus Question: Setup downtime
Downtime 7pm - 9am Monday to Friday:
![alt text](https://i.imgur.com/Ix28kgg.png"")

Downtime Full day off on Weekend:
![alt text](https://i.imgur.com/PsQfD62.png"")

Email: (Time is UTC and not local time zone GMT+1)
![alt text](https://i.imgur.com/xm071fj.png"")
Reference info:
https://docs.datadoghq.com/monitors/
https://docs.datadoghq.com/monitors/downtimes/?tab=recurring#pagetitle

## Collecting APM 

I installed ddtrace and flask using the following commands: 
```bash
pip install ddtrace
pip install flask
```
The I created the flask app from the hiring challenge: 
```python 
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
```
I then started the flask app with ddtrace running using the following command and parameters: 
```bash
DD_SERVICE="flask" DD_ENV="prod" DD_LOGS_INJECTION=true ddtrace-run python flask_test.py
```
Now we can see the server starting with ddtrace active.
![alt text](https://i.imgur.com/SQdnWJN.png"")

I then used curl on another window to test the endpoints:
![alt text](https://i.imgur.com/MvflIKu.png"")

These request were successfully traced and create the following dashboards
![alt text](https://i.imgur.com/SlyvdTS.png"") 

![img](https://i.imgur.com/No5Jgls.png)

I then created my own dashboard to show the data. This can be found at https://app.datadoghq.eu/dashboard/ynj-ssk-svj/apm?from_ts=1621237011835&live=true&to_ts=1621240611835. 
![alt text](https://i.imgur.com/qu7aE8D.png"")


Reference info:
https://docs.datadoghq.com/tracing/

#### Bonus: difference between service and Resource
A service is a set of processes that do similar jobs whereas a Resource is a particular action for a given service.
Reference info:
https://docs.datadoghq.com/tracing/visualization/resource/
https://docs.datadoghq.com/tracing/visualization/service/
https://docs.datadoghq.com/tracing/visualization/#services

## Challenges during the challenge 
#### System ran out of disk space
My systems diskspace filled up when starting the challenge causing my virtual machine to stall. The cause was not obvious at first but once I checked the virtual box logs I noticed the issue quickly and deleted some files from my laptop.
#### Posting dashboard to US servers
Initially I struggled with posting dashboards as I was posting to the US API at: 
```
https://api.datadoghq.com/api/v1/dashboard
```
After a deep dive into the documentation I realized my mistake and corrected it and started posting to:
```
https://api.datadoghq.eu/api/v1/dashboard
```
#### Datadog-trace service failing
On my initial attempt I reached the APM section but was unable to complete it due to the datadog-agent-trace service instantly failing on restart. 
![alt text](https://i.imgur.com/VxXj0Kh.png "")

I tried to debug this issue but was unsuccessful and the logs yielded little value. There is a lot of documents on debugging the tracer once it is active but found it hard to get documents on the tracer errors prior to startup.
To get around this, I destroyed the VM and restarted from fresh. This workaround avoided the issue but did not result in a root cause. 

## Final Question 
I think a creative use could be to use datadog to track content delivery across a museum/Art gallery. A lot of museums rely on a QR code system to guide viewers to online resources / audio tours to provide easy access to information about an exhibit. The system could be used to track the stability of this content delivery and detect failed requests. This would help identify broken links or issues allowing them to maintain the exhibit to match its potential. Additionally, It would allow you to track the movement/ time spent of the patrons around the exhibits which may provide valuable feedback on user interests

On the commercial side, I think only public institution and high end galleries would have the resources/financial backing to run such a system and have the requirement for near 100% uptime.