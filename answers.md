**Section I: Collecting Metrics**

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**
My host tags can be seen here: https://la-psql-zebra.s3.amazonaws.com/host_tags.PNG

I choose to install PostgreSQL and installed the Datadog integration for Postgres. This can be verified in Section II by viewing my dashboard. 
Here is my_metric.py https://github.com/ekufta0530/hiring-engineers/blob/master/my_metric.py
```python
import random
import datadog_checks.base import AgentCheck

class MyCheck(AgentCheck):
      def check(self, instance):
              self.gauge('my_metric', random.randint(0, 1000))
```


`Bonus Question` Can you change the collection interval without modifying the Python check file you created? Yes, I modified conf.d/my_metric.yaml to include - 
...
min_collection_interval: 45. 
...

**Section II: Visualizing Data**
Here is the link to the script I used to generate the timeseries. https://github.com/ekufta0530/hiring-engineers/blob/master/timeboard_script
Snapshot of my dashboard: https://la-psql-zebra.s3.amazonaws.com/my_first_dashboard_5min.PNG
`Bonus Question`: What is the Anomaly graph displaying?
The anomoly graph is displaying expected behavior in shaded area and actual as the line.

**Section III: Monitoring Data**
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:


