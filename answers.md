Your answers to the questions go here.
## Table of Contents
* [Setting Up the Environment](#setting-up-the-environment)
* [Collecting Metrics](#collecting-metrics)
* [Visualizing Data](#visualizing-data)
* [Monitoring Data](#monitoring-data)
* [Collecting APM Data](#collecting-apm-data)
* [Final Question](#final-question)

<a name="setting-up-the-environment"/>

## Prerequisites - Setting Up the Environment
1. First, I spinned up a fresh linux Ubuntu VM via Vagrant on Virtual Box on my Mac. I followed these steps: https://medium.com/devops-dudes/how-to-setup-vagrant-and-virtual-box-for-ubuntu-20-04-7374bf9cc3fa
2. Next, I signed up for Datadog (used “Datadog Recruiting Candidate” in the “Company” field). 
3. And installed the Datadog Agent on the  Vagrant Box by running this command for ubuntu:  
```DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=########## DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"```  
I removed the key for security purposes.
4. Finally, got the Agent reporting metrics from my local machine:
<img src='./screenshots/Agent Reporting Metrics.png'> </img>

<a name="collecting-metrics"/>

## Collecting Metrics
1. Added tags in the Agent config file and here is the screenshot of the host and its tags on the Host Map page in Datadog.
<img src='./screenshots/Datadog Agent Yaml Tags 1.png'> </img>
<img src='./screenshots/Datadog Yaml Tags 2.png'> </img>
<img src='./screenshots/Datadog Dashboard Tags.png'> </img>

2. Installed PostgreSQL on the Vagrant machine and then installed the respective Datadog integration for that database.
    - Added the public GPG key:  
    ```wget -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -```
    - Created a file with the repository address:  
    ```echo deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main | sudo tee /etc/apt/sources.list.d/postgresql.list```
    - To install PostgreSQL I ran:  
    ```sudo apt-get update```   
    ```sudo apt-get install postgresql-9.3 postgresql-contrib-9.3```
    - After installing PostgreSQL, I ran the following command to create a user for Datadog in the database.  
    ```create user datadog with password ‘######’;```
3. Created a script file and a config file in order to create a custom metric and send it to Datadog servers through the Agent.

<img src='./screenshots/Postgres conf.d.png'></img>

After ```mymetric.py``` was created ```~/.datadog-agent/checks.d/mymetric.py``` added the following to the file:

<img src='./screenshots/mymetric.py.png'></img>

Then I created ```mymetric.yaml ~/.datadog-agent/conf.d/mymetric.yaml``` and added the code below.

<img src='./screenshots/mymetric yaml.png'></img>

After I restarted the Agent.
<img src='./screenshots/mymetric Dashboard.png'></img>

On the Datadog dashboard, I went to ```Metrics > Explorer```, and searched for my custom metric.
The Agent was running the collector in intervals of 15–20 seconds.

4. To change my check’s collection interval I edited the config file ```~/.datadog-agent/conf.d/mymetric.yaml``` and changed the ```min_collection_interval``` globally to the interval of 45 seconds.

<img src='./screenshots/mymetric yaml 45 interval.png'></img>

    And restarted the Agent again.
<img src='./screenshots/mymetric Dashboard 45 Interval.png'></img>

5. Bonus Question: Can you change the collection interval without modifying the Python check file you created?
    Yes, the interval can be set by changing the instance description in the ```yaml``` file, like this:
```
    init_config:
            min_collection_interval: 45
    instances:
    [{}]
```

<a name="visualizing-data"/>

## Visualizing Data
1. This board was created using the PostMan API editor.
<img src='./screenshots/Postman API Editor.png'> </img>
To create my dashboard I used the content of this curl command:
    ```
    curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: DD-PSHARD=217' \
    --header 'DD-API-KEY: xxxxxxxxxxxxxxxxxxxxxxxxxx' \
    --header 'DD-APPLICATION-KEY: xxxxxxxxxxxxxxxxxxxxxxxxxx' \
    --data-raw '{
        "title": "Dev.Zarudnaya Hourly Anomalies",
        "description": "A custom agent check configured to submit a metric named `my_metric` with a random value between 0 and 1000.",
        "layout_type": "ordered",
        "is_read_only": false,
        "widgets": [
            {
                "definition": {
                    "type": "timeseries",
                    "title": "my metric timeseries",
                    "requests": [
                        {
                            "q": "my_metric{host:datadog.dev.zarudnaya.info}"
                        }
                    ]
                },
                "layout": {
                    "x": 0,
                    "y": 0,
                    "width": 4,
                    "height": 2
                }
            },
            {
                "definition": {
                    "type": "timeseries",
                    "title": "Postgres Sql Return Rows Anamolies",
                    "requests": [
                        {
                            "q": "anomalies(sum:postgresql.rows_returned{host:datadog.dev.zarudnaya.info}, '\''basic'\'', 5)"
                        }
                    ]
                },
                "layout": {
                    "x": 4,
                    "y": 0,
                    "width": 4,
                    "height": 2
                }
            },
            {
                "definition": {
                    "type": "timeseries",
                    "title": "Sum of my metric points per hour",
                    "requests": [
                        {
                            "q": "sum:my_metric{*}.rollup(sum, 3600)"
                        }
                    ]
                },
                "layout": {
                    "x": 8,
                    "y": 0,
                    "width": 4,
                    "height": 2
                }
            }
        ]
    }'
    ```

2. Once this was created, I accessed the Dashboard from the Dashboard List in the UI:
   ##### My Hourly Timeboard
   <img src='./screenshots/My Hourly Timeboard.png'> </img>

3. The sum of my metric is grouped into hours (per instructions) so it did not show properly in a 5 minute time span. I expanded the time period on the widget and included a snapshot here.
    <img src='./screenshots/mymetric sum.png'> </img>

4. Took a snapshot of this graph and used the @ notation to send it to myself. The email notice included a thumbnail, and also buttons that take you directly to the item in the Datadog panel.
    <img src='./screenshots/Email notice of snapshot anamolies.png'> </img>

5. Bonus Question: What is the Anomaly graph displaying?  
    The Anomaly graph presents suspicious behaviour. I stressed PostgreSQL and made the tables list, thus, causing it to perform in a certain way. The graph provides a visualization of this performance as it relates to PostgreSQL.

<a name="monitoring-data"/>

## Monitoring Data
#### Create a New Metric:
1. From Datadog dashboard ```Monitors > New Monitor > Metric Monitor > Metric``` I defined the specs for ```my_metric``` based on the requirements.
    - Changed the metric to the custom metric ``my_metric``.
    - Changed the warning threshold to 500.
    - Changed the alerting threshold to 800.
    - Ensured notifications for No Data past 10 minutes.

#### Monitor Metrics:
<img src='./screenshots/Monitor metric Dashboard Timeboard.png'> </img>
<img src='./screenshots/Monitor metric Dashboard Timeboard 2.png'> </img>

#### Configure the Monitor's Message:
2. I configured the monitor message with below settings:
<img src='./screenshots/Configure the monitor Message.png'> </img>

#### Monitor Message Email Notifications
3. Created different messages based on whether the monitor is in an Alert, Warning, or No Data state.

#### Alert:  
<img src='./screenshots/Alert Email.png'> </img>

#### Warning:  
<img src='./screenshots/Warn Email.png'> </img>

#### Missing Data:  
<img src='./screenshots/Missing Data Email.png'> </img>

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:  
#### Downtime Settings: 
1. From Datadog dashboard ```Monitors > Manage Downtime``` clicked 'Schedule Downtime':  

<img src='./screenshots/Downtime setting dashboard.png'> </img>

2. Created a recurring downtime for days of the week and weekends. I used EST since this is my time zone and Datadog HQ time zone.  
#### Downtime Weekday Settings:
<img src='./screenshots/Downtime Weekday Settings.png'> </img>

#### Downtime Weekend Settings:
<img src='./screenshots/Downtime Weekend Settings.png'> </img>

<a name="collecting-apm-data"/>

## Collecting APM Data

 





    













