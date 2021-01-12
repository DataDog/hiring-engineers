## Prerequisites - Setup the environment

#### 1) Installed vagrant and virtualbox
#### 2) Initialized a project configured a project 
<img width="512" alt="vagrant_virtualbox_running" src="https://user-images.githubusercontent.com/76797887/103483463-63941300-4db5-11eb-8758-f9b90e660db9.png">

#### 3) Added host to datadog
<img width="650" alt="environment" src="https://user-images.githubusercontent.com/76797887/103483751-71e32e80-4db7-11eb-94c9-d0c38a644271.png">

## Collecting Metrics: 

#### 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

#### >Agent Config File
<img width="650" alt="Screen Shot 2020-12-23 at 12 20 57 AM" src="https://user-images.githubusercontent.com/76797887/103392132-6c9d8f80-4aea-11eb-80f2-d8a0e50b0d76.png">

#### >Host Map page in Datadog
<img width="650" alt="Screen Shot 2020-12-23 at 12 23 17 AM copy" src="https://user-images.githubusercontent.com/76797887/103392293-15e48580-4aeb-11eb-9392-9f1e597be75a.png">

#### 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

#### >Installed MySQL on host
<img width="579" alt="Screen Shot 2020-12-24 at 1 29 02 PM" src="https://user-images.githubusercontent.com/76797887/103392915-04e94380-4aee-11eb-8e21-63316e2facce.png">

#### >Installed and configured datadog mySQL integration
<img width="579" alt="Screen Shot 2020-12-24 at 1 19 39 PM" src="https://user-images.githubusercontent.com/76797887/103392929-1a5e6d80-4aee-11eb-8964-ad118ca5a33e.png">

#### >sudo datadog-agent status 
#### >mysql metrics available and running
<img width="579" alt="Screen Shot 2020-12-24 at 2 25 50 PM" src="https://user-images.githubusercontent.com/76797887/103393089-e899d680-4aee-11eb-8f6a-a8a372dc3f89.png">

#### >Enabled mySQL logging  
<img width="579" alt="Screen Shot 2020-12-24 at 2 24 47 PM" src="https://user-images.githubusercontent.com/76797887/103393095-f0f21180-4aee-11eb-9798-9b4cde98ea54.png">


#### 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

#### >Documentation used: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
#### >Created a my_metric conf.d (yaml) and checks.d (python) file required for a custom metric
#### >my_metric conf.d file
<img width="444" alt="my_metricconf" src="https://user-images.githubusercontent.com/76797887/103393254-c5bbf200-4aef-11eb-8033-1aed34d816c7.png">

#### >my_metric checks.d file
<img width="444" alt="mymetriccheks" src="https://user-images.githubusercontent.com/76797887/103393300-ef751900-4aef-11eb-95a6-73067eaed009.png">

#### >Verified that my_check created is running properly with 'sudo datadog-agent status'
<img width="444" alt="Screen Shot 2020-12-24 at 1 01 32 PM" src="https://user-images.githubusercontent.com/76797887/103393338-2e0ad380-4af0-11eb-948a-b07b97134845.png">

#### 4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

#### >Edit the "min_collection_interval" in my_metric conf.d file
<img width="444" alt="Screen Shot 2020-12-23 at 1 15 29 AM" src="https://user-images.githubusercontent.com/76797887/103393476-d0c35200-4af0-11eb-8150-b12bd235f96e.png">

#### >my_metric displayed 
<img width="500" alt="my_metricgraph" src="https://user-images.githubusercontent.com/76797887/103393540-09632b80-4af1-11eb-8287-542ded895d8e.png">

#### BONUS Question: Can you change the collection interval without modifying the Python check file you created?

#### A) Yes, you can do it in the check configuration file by defining “min_collection_interval” like in the picture above.

## Visualizing Data:

#### 1) Create a Timeboard using the datadog API with the following graphs

* Your custom metric scoped over your host.
<img width="444" alt="my_metric over host" src="https://user-images.githubusercontent.com/76797887/103484525-6bf04c00-4dbd-11eb-8f1a-fcc0de207bd7.png">

* Any metric from the Integration on your Database with the anomaly function applied.
<img width="444" alt="anomalie graph" src="https://user-images.githubusercontent.com/76797887/103484523-6bf04c00-4dbd-11eb-8359-7406732e48f7.png">

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
<img width="444" alt="hourly roll-up" src="https://user-images.githubusercontent.com/76797887/103484524-6bf04c00-4dbd-11eb-9627-43b5298f3136.png">

#### 2) Provide the API script used to create timeboard 
```
curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--header 'Cookie: DD-PSHARD=151' \
--data-raw '{
    "title": "Aainys_Timeboard",
    "layout_type": "ordered",
    "notify_list": [
        "saainyzahra@gmail.com"
    ],
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {"q": "my_metric{host:ubuntu1604.localdomain}"}
                ],
                "title": "my_metric over host",
                "title_align": "center"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.performance.cpu_time{host:ubuntu1604.localdomain}, '\''basic'\'', 2)"
                    }
                ],
                "title": "mysql cpu performance anomolies",
                "title_align": "center"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                 "time": {

                    "live_span": "4h"

                },
                "requests": [
                    {
                        "q": "sum:my_metric{host:ubuntu1604.localdomain}.rollup(sum,3600)"
                    }
                ],
                "title": "hourly roll up for sum of my_metric over host ",
                "title_align": "center"
            }
        }
    ]
}'
```

#### 3) Access the Dashboard from your Dashboard List in the UI:
* Set the Timeboard's timeframe to the past 5 minutes
<img width="1278" alt="Screen Shot 2021-01-03 at 2 51 11 PM" src="https://user-images.githubusercontent.com/76797887/103487433-70bffa80-4dd3-11eb-8117-2f334d2585a7.png">

* Take a snapshot of this graph and use the @ notation to send it to yourself.

<img width="450" alt="Screen Shot 2021-01-03 at 2 54 32 PM" src="https://user-images.githubusercontent.com/76797887/103487469-b7155980-4dd3-11eb-9640-ce49ecca83f7.png">

**Email notification**

<img width="450" alt="Screen Shot 2021-01-03 at 2 55 14 PM" src="https://user-images.githubusercontent.com/76797887/103487488-d8764580-4dd3-11eb-8033-bd31e8cc8392.png">

* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data:

#### 1) Used the following documentation: 

* Monitor Creation: https://docs.datadoghq.com/monitors/monitor_types/metric/?tab=threshold
* Alerting Notifications: https://docs.datadoghq.com/monitors/notifications/?tab=is_alert#conditional-variables
* Downtimes: https://docs.datadoghq.com/monitors/downtimes/?tab=bymonitorname

#### 2) Created the monitor via the UI

<img width="1286" alt="Screen Shot 2021-01-04 at 4 42 04 PM" src="https://user-images.githubusercontent.com/76797887/103582571-1f376e80-4eac-11eb-82a6-8e6a468a2141.png">

#### 3) Exported the JSON

```json
{
	"id": 0,
	"name": "my_metric monitor ",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:ubuntu1604.localdomain} > 800",
	"message": "{{#is_alert}} \nmy_metric ( {{value}} ) on host {{host.ip}} is too high! \n{{/is_alert}}\n\n{{#is_warning}}\nmy_metric ({{value}} ) on {{host.ip}} is OKAY-- but is nearing cirtical state. Please investigate. \n{{/is_warning}} \n\n{{#is_no_data}}\nmy_metric has not reported data in the last 10+ minutes.\n{{/is_no_data}}   \n\n@saainyzahra@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": false,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	},
	"priority": null
}
```

#### 4) Monitor email notification

<img width="536" alt="Screen Shot 2021-01-04 at 4 56 49 PM" src="https://user-images.githubusercontent.com/76797887/103583626-07f98080-4eae-11eb-8daa-098015983a33.png">

#### Bonus: Configure Monitor Downtime

###### 1) Silenced from 7pm to 9am daily on M-F


<img width="554" alt="Screen Shot 2021-01-04 at 5 08 24 PM" src="https://user-images.githubusercontent.com/76797887/103585143-94a53e00-4eb0-11eb-9c97-f3cc37c52831.png">

###### 2) Silenced Sat-Sun

<img width="537" alt="Screen Shot 2021-01-04 at 5 10 00 PM" src="https://user-images.githubusercontent.com/76797887/103585213-adadef00-4eb0-11eb-8029-3c415a0fff48.png">

###### 3) Screenshot of email notification.

<img width="566" alt="Screen Shot 2021-01-04 at 5 14 59 PM" src="https://user-images.githubusercontent.com/76797887/103585257-bef6fb80-4eb0-11eb-9c65-21b5f3e33a12.png">

## Collecting APM Data

I was unable to instrument an application with the APM after numerous attempts. 

* **BONUS QUESTION: Difference between resource and service** 

** Service are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.

** Resource represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.
** source:https://docs.datadoghq.com/tracing/visualization/

## Final Question

* **Unique use for Datadog**
