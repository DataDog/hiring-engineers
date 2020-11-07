Your answers to the questions go here.

<!-- python script to send random number 0-1000 -->

# the following try/except block will make the custom check compatible with any Agent version

try: # first, try to import the base class from new versions of the Agent...
from datadog_checks.base import AgentCheck
except ImportError: # ...if the above failed, the check is running in Agent version < 6.6.0
from checks import AgentCheck

# content of the special variable **version** will be shown in the Agent status page

**version** = "1.0.0"

```
import random

class CustomMyMetricCheck(AgentCheck):
    def check(self, instance):
        randomNum = random.randint(0,1000)
        self.gauge('random.number', randomNum, tags=['RandomKey:RandomValue'])
~
~
~
~
"custom_my_metric.py" 17L, 668C

```

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

using the DataDog Postman API package I generated the Tiemboard using the Dashboard Post endpoint

```
{
    "title": "API TIMEBOARD SINGLE GRAPH w/style",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*} by {data_cat}.rollup(sum, 3600)",
                        "style": {
                            "palette": "warm",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "avg:my_metric{*}",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:postgresql.db.count{*}, 'basic', 2)",
                        "style": {
                            "palette": "orange",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "title": "My Metric - Roll up 1hr (3600 sec), Instance, PostgreSQL DB Size: Anomaly fn"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "Timeboard API",
    "is_read_only": true,
    "notify_list": [
        "J.Tustin@gmail.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "vagrant"
        }
    ]
}
```
