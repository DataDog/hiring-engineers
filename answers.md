Your answers to the questions go here.
## Collecting Metrics
1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Link: https://app.datadoghq.com/infrastructure/map?host=652858656&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Link: https://app.datadoghq.com/account/settings#integrations

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

In order to create a custom Agent check, I read the documentation and created the directory checks.d and has a file called custom_check.py. I also created a custom_check.yaml
As you can see in the screenshot for the code, I generated a random value between 0 and 1000 using self.gauge to sample the metric.
4. Change your check's collection interval so that it only submits the metric once every 45 seconds.
As you can see in the code that I used the sleep method imported from the time module, I changed the Python script to change the collection interval of 'my_metric' every 45 seconds.

Bonus Question:
Can you change the collection interval without modifying the Python check file you created?
In order to set the interval without modifying the python check file, you would just modify the custom_check.yaml file adding the min_collection_interval.


## Visualizing Data
Utilize the Datadog API to create a Timeboard that contains:
1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.
-- look at the screenshot
-- also screenshot of the timeBoard file.

Bonus Question: What is the Anomaly graph displaying?
Answer: The Anomaly function shows there are unusual trends outside of the normal range of values.
The unusual trends are represented by red peaks and troughs on the graphs whereas the normal ranges are outlined in blue.


## Monitoring
