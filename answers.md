# Index:

* [Prerequisites](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#prerequisites---setup-the-environment)
* [Collecting Metrics](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#collecting-metrics)
    1. [Setup agent](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#1-setup-agent)
    2. [Setup DB integration](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#2-setup-db-integration)
    3. [Setup custom Agent](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#3-setup-custom-agent)
    4. [Change collection interval](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#4-change-collection-interval)
* [Visualizing Data](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#visualizing-data)
    1. [Dashboard script](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#dashboard-script)
    2. [Dashboard](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#dashboard)
* [Monitoring Data](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#monitoring-data)
    1. [Create Monitor](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#create-monitor)
    2. [Notifications example](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#warning-notification)
    3. [Bonus task](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#bonus)
* [Collecting APM data](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#collecting-apm-data)
    1. [APM Config and Python trace](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#apm-config-and-python-trace)
    2. [APM Dashboard](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#apm-dashboard)
* [Final Question](https://github.com/pkishino/hiring-engineers/blob/master/answers.md#final-question)



## Prerequisites - Setup the environment

For this part I spun up a simple ubuntu vm in [proxmox](https://www.proxmox.com/en/) as I already had it setup and in use for a few other containers/vms that I run.
<img width="1226" alt="setup" src="https://user-images.githubusercontent.com/4121314/154208933-1207bfea-dcde-4c23-94dc-b5e1eb730b9d.png">



## Collecting Metrics:

### *1) Setup agent*

After following the [official guidelines](https://docs.datadoghq.com/getting_started/agent/) for getting the Ubuntu agent installed and the agent started reporting, I added a few tags to the .yaml config file as seen below
<img width="1282" alt="Screen Shot 2022-02-16 at 15 24 25" src="https://user-images.githubusercontent.com/4121314/154209220-6c624013-a01a-4ce4-83f5-75480babb24e.png">

### *2) Setup DB integration*

Next I proceeded to install and start [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) as a service, setup the MongoDB integration and add some [data](https://media.mongodb.org/zips.json) to MongoDB.
I've used MongoDB in one form or another in various projects in the past, especially in docker containers. But for this I went with a simple baremetal install.
There were some initial complications here as apt was using the new MongoDB v5 which requires a newer CPU architecture than I had on my proxmox, so it took some time fiddling around to downgrade to a previous, working version.

<img width="896" alt="Screen Shot 2022-02-16 at 21 16 10" src="https://user-images.githubusercontent.com/4121314/154262808-5e0919c0-4c11-4efc-ba96-5f34a75ae9fc.png">

<img width="1274" alt="image" src="https://user-images.githubusercontent.com/4121314/154266083-650c3539-2d6c-4622-8529-73369c7fd223.png">

### *3) Setup custom Agent*

Next, I proceeded to check the [documentation on custom agents](https://docs.datadoghq.com/developers/custom_checks/write_agent_check) and created a simple metric providing random numbers.
<img width="445" alt="image" src="https://user-images.githubusercontent.com/4121314/154276144-de0a52d1-cee3-4a7b-82c7-a68843689723.png">

Re-using the example and adding a simple [random number generator](https://docs.python.org/3/library/random.html), I got the metric showing in the dashboard.

<img width="834" alt="image" src="https://user-images.githubusercontent.com/4121314/154276923-a1fd0f74-1512-4f34-9148-d911e287028c.png">

### *4) change collection interval*

Following [here](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval) it was straightforward to change the interval in the .yaml config. No need to modify the python file.
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
<img width="94" alt="Screen Shot 2022-02-16 at 22 45 42" src="https://user-images.githubusercontent.com/4121314/154277523-41f740a2-2130-49ef-b7fe-e1a229cd7f2b.png"> <img width="85" alt="Screen Shot 2022-02-16 at 22 45 48" src="https://user-images.githubusercontent.com/4121314/154277534-213ff472-6f9a-4a4c-90ac-e36ce364175e.png">

**Comment:** While it should, according to [documentation](https://docs.datadoghq.com/metrics/summary/#interval) be possible to set metric metadata interval via the GUI, it did not seem to have any effect.

## Visualizing Data:

*Task*:

```
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```
First of all, I looked in the API documentation for Timeboards but moved on to [Dashboards](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard) as timeboards have been deprecated in favour of them.
Based on the great examples there, I chose to re-use the Python example and adapted it to my metric.

Reading [this](https://datadog-api-client.readthedocs.io/en/latest/) helped to understand and customise the python script using the datadog_api_client library.
Besides my custom metric, I decided to include the mongodb.connections.available metric.

[This](https://docs.datadoghq.com/dashboards/functions/algorithms/#anomalies) page helped to clarify the request parameters for the anomalies query and based on [this](https://docs.datadoghq.com/monitors/create/types/anomaly/#anomaly-detection-algorithms) I decided to just use the 'basic' algorithm with '2' as the bounds.

Finally, [this](https://docs.datadoghq.com/dashboards/querying/#rollup-to-aggregate-over-time) showed how to do the rollup for my_metric.

   ### Dashboard script

The below script is the result
```python
"""
DataDog homework dashboard script
"""
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_sort import WidgetSort
host="{host:devmachine}"
body = Dashboard(
    layout_type=DashboardLayoutType("ordered"),
    title="DataDog Sales Engineer Assignment Dashboard",
    widgets=[
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="My Metric Widget",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{}".format(host)
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="MongoDB connections available+anomalies",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(mongodb.connections.available{}, 'basic', 2)".format(host)
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="My Metric rollup sum for past 60 minutes",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{}.rollup(sum,3600)".format(host)
                        )
                ],
            )
        )
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)
```

   ### Dashboard
[LINK to the dashboard](https://p.datadoghq.eu/sb/40be0dc8-8ee5-11ec-a2e0-da7ad0900005-620a06d2d9298e6f3e327a9a244cd937)
<img width="1261" alt="Screen Shot 2022-02-17 at 21 08 23" src="https://user-images.githubusercontent.com/4121314/154479777-78b970d4-a3f9-4c44-8d87-7cfd61c7a581.png">

<img width="720" alt="image" src="https://user-images.githubusercontent.com/4121314/154480081-fe000329-5502-4011-a8fd-716458c8e9cb.png">

   ### **Bonus Question**: *What is the Anomaly graph displaying?*

The Anomaly graph shows the current data (the blue line in my dashboard) with a gray band around it (in my case set to 2, which can be interpreted as the standard deviation of the 'basic' algorithm specified). Any data point that is beyond the gray band would be an anomaly,marked in red, and should be investigated.

## Monitoring Data

*Task*:

>Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

>* Warning threshold of 500
>* Alerting threshold of 800
>* And also ensure that it will notify you if there is No Data for this query over the past 10m.

   ### Create Monitor
This part was quite easy as the GUI is very intuitive.
<img width="1133" alt="Screen Shot 2022-02-17 at 21 25 57" src="https://user-images.githubusercontent.com/4121314/154481542-cf1017f2-946f-4757-bd6d-3f6340f1840d.png">
<img width="1245" alt="image" src="https://user-images.githubusercontent.com/4121314/154484427-065cd222-28df-476d-9b44-df4a61c72ea9.png">


[LINK](https://app.datadoghq.eu/monitors/4484135) to the finished monitor

   ### Warning notification

<img width="714" alt="image" src="https://user-images.githubusercontent.com/4121314/154484591-f7c4f496-9ce7-4acf-894a-af5b5da99a8f.png">



   ### Bonus
>* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

 > * One that silences it from 7pm to 9am daily on M-F,
  >* And one that silences it all day on Sat-Sun.
  >* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Again, down to intuitive GUI, this was easily acomplished in the Monitor Menu: Manage Downtimes>Schedule Downtime 
First one I setup as a weekly occurance on M-F, second on Sat/Sun exclusivly
<img width="720" alt="image" src="https://user-images.githubusercontent.com/4121314/154485960-3f1b6115-c9b9-444e-a725-015d2f134bb8.png">
<img width="717" alt="image" src="https://user-images.githubusercontent.com/4121314/154486347-558b8c6e-0275-4c79-9d4d-23198b1d4cfd.png">


*Comment: Email shows times in UTC*

<img width="719" alt="Screen Shot 2022-02-17 at 21 55 48" src="https://user-images.githubusercontent.com/4121314/154486507-9a23b79b-3e41-42b6-9675-ca7e89d49481.png">



## Collecting APM Data:

   ### APM Config and Python trace
Following [this documentation](https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers) it was straight forward to add the [Flask app](https://github.com/pkishino/hiring-engineers/blob/master/assignmentFlask.py), enable apm_config in the datadog.yaml 

<img width="976" alt="image" src="https://user-images.githubusercontent.com/4121314/154599022-42a21276-7012-422c-b262-38f96fb21858.png">

<img width="915" alt="image" src="https://user-images.githubusercontent.com/4121314/154599401-fff69792-26ed-43b1-8c62-834e26a8ed04.png">

   ### APM Dashboard
After this I cloned the host Dashboard and added the APM metrics widgets via the GUI.
[Dashboard](https://app.datadoghq.eu/dashboard/hqs-jc9-kmk?from_ts=1645146654974&to_ts=1645148454974&live=true)
<img width="1269" alt="image" src="https://user-images.githubusercontent.com/4121314/154601384-4306a91b-f9bd-4a71-8507-c9501e424a69.png">

* **Bonus Question**: What is the difference between a Service and a Resource?

In my own words:
 A *Resource* is some kind of result or actual value which can be consumed by *Services* which in turn provide a functionality that can be combined to create *Applications*.
 
 Per the [APM Glossary](https://docs.datadoghq.com/tracing/visualization/)
>Service Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.

>Resource	Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
