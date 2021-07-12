# Madeline Lee Technical Exercise Answers

## Prerequesites: Setting Up the Environment

I used a vagrant box for this exercise. I installed the agent on it using:
`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<REDACTED> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"`

 
## Collecting Metrics

### Adding Tags
When adding tags to the config file to have it show up in the host map, I referenced [this help article](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-files) for documentation. However, I noticed my tags were not showing up. This is when I realized that my config file was not going to take string quotes in the form of `"<KEY>: <VALUE"`, it just took raw text like `<KEY>:<VALUE>`. This tripped me up after trying several iterations, `"KEY":"VALUE"`, `<KEY>:"VALUE"`, etc.

 However I was able to get the tags to show up on the host map. Interestingly, while it was intuitive that I had to restart the agent on the vagrant box, I also had to refresh the browser to see all the tags once I had typed them into the search bar.
 ### Installing Postgres
 
 To install Postgres, I used [this reference](https://www.postgresql.org/download/linux/ubuntu/):
 
 with these commands:
 
```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -OK

$sudo apt-get -y install postgresql'
```

Once in the Postgres instance, I created the datadog user and gave it access to monitor the instance using commands from [this reference](https://docs.datadoghq.com/integrations/postgres/?tab=host).

```
postgres=# create user datadog with password 'datadog';
CREATE ROLE
postgres=# grant pg_monitor to datadog;
GRANT ROLE
postgres=# grant SELECT on pg_stat_database to datadog;
GRANT
```

Then, I edited the yaml file to include postgres using `$ sudo nano /.datadogagent/conf.d/postgres.d/conf.yaml`
To be honest, when I read the instructions to edit the 'postgres.d/conf.yaml' file I did not understand that it was an extension of the conf.d file. Only when I did a google search and read this [medium article](https://zero2datadog.readthedocs.io/en/latest/collect.html) with the quote "Edit the `~/.datadog-agent/etc/conf.d/mysql.d/conf.yaml.`" did I understand that the 'postgres.d/conf.yaml' had to be appended to the agent config file. Was this a small brain moment? Either way, thanks Blaise Pabon.

### Creating a Custom Agent Check
I ran into the same problem as many before me (see [here](https://www.reddit.com/r/datadog/comments/91hezx/custom_agent_check_help/) and could not figure out where to put the yaml and the py file. After reading this thread it was pretty straightforward.

First, I created the yaml file and named it 'custom_check_value.yaml':
```
init_config:

instances:
   [{}]
```
   
Then, I created the .py file and named it 'custom_check_value.py' (modified code from the [Datadog Summit Training Docs](https://datadoghq.dev/summit-training-session/handson/customagentcheck/))

```
try:

   from datasog_checks.base import AgentCheck

except ImportError:
   from checks import AgentCheck

import random

__version__ = '1.0.0'

class HelloCheck(AgentCheck):
   def check(self, instance):
      self.gauge('my_metric', random.randint(0,1000), tags=["env:qa", "metric_submission_type:gauge"])
 ```
      
### Changing the Collection Interval
I changed the collection interval by editing the yaml file to read:
```
init_config:

instances:
   -min_collection_interval: 45
   ```
   
## Visualizing Data

### Using the API to create a Dashboard
I used postman to format my API calls. First, I created the simplest widget - a free text box, to make sure I was sending calls correctly.

You can find this dashboard here: https://p.datadoghq.com/sb/d20d36ac-dbba-11eb-ad10-da7ad0900002-6c38f09d6779b5c8b1c024f896241af1
API Call:

```
curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'DD-API-KEY: <REDACTED> \
--header 'DD-APPLICATION-KEY: <REDACTED>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "my first dashboard",
    "is_read_only": false,
    "layout_type": "ordered",
    "title": "the title",
    "widgets": [
        {
            "definition": {
                "color": "green",
                "font_size": "18",
                "text": "the text box",
                "text_align": "left",
                "type": "free_text"
            },
            "id": 1234,
            "layout": {
                "height": 10,
                "is_column_break": false,
                "width": 9,
                "x": 0,
                "y": 0
            }
        }
    ]
}'
```

After reading the sample documentation on timeseries, I went in search of some example dashboards. I created a dashboard in the UI and saw that there was json formatting for a timeseries visualization, so I copied that to put in my API call. 

This is what the json looked like:

```
{
    "viz": "timeseries",
    "requests": [
        {
            "formulas": [
                {
                    "formula": "query1"
                }
            ],
            "queries": [
                {
                    "data_source": "metrics",
                    "name": "query1",
                    "query": "avg:my_metric{*}"
                }
            ],
            "response_format": "timeseries",
            "type": "line",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            }
        }
    ],
    "yaxis": {
        "scale": "linear",
        "min": "auto",
        "max": "auto",
        "include_zero": true,
        "label": ""
    },
    "markers": []
}
```

However, I ran into errors when copy-pasting this into the body of the API call, some listed below:

` ‘Invalid widget definition at position 0 of type timeseries. Error: additional properties are not allowed (u ‘viz’ was unexpected).`

```{"errors": ["Invalid widget definition at position 1 of type timeseries. Error: {u'formulas': [{u'formula': u'query1'}], u'queries': [{u'query': u'avg:my_metric{*}', u'data_source': u'metrics', u'name': u'query1'}]} is not valid under any of the given schemas."]}
```

After reading through the documentation on timeseries and queries, I realized that the json that i had copy-pasted used formulas and queries, which were still in beta. So i ended up writing my own formatting json calls. I heavily referenced this [example on medium](https://zero2datadog.readthedocs.io/en/latest/visualize.html#visualize-data-with-the-web-ui) for help with syntax, as I simply could not find any examples with real queries in the Datadog API documentation.

Final Dashboard API Call:

Note that I used timeseries and query value widgets for the Rollup function - for the rollup function, if you filter to the past 5 minutes, you don't tend to see data on the timeseries (what if you looked at this at 16:25, for example?). If you filter to the past 4 hours or greater time frame, the timeseries for the rollup function is interesting. However, at any other time filter, It would not show data. So, I included the query value widget so that the end user has a KPI that they 
can reference at any point that they view the dashboard with any filter.

When I first wrote the json for the anomaly function for postgres, I wasn't seeing data populate through the viz - because I hadn't put any recent traffic on the postgres instance. To double check that I had written the json correctly, I created an anomaly function for my custom metric. When this was verified that it was working, I simply put more traffic on the postgres instance and then saw the viz populate afterwards. 

I kept all of my test visualizations on the final version and all and dashboard versions in my datadog dashboards list for a look at my thought process. 

link: https://p.datadoghq.com/sb/d20d36ac-dbba-11eb-ad10-da7ad0900002-275af4cc01dac66435c6c5c3415f52e3

```
curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'DD-API-KEY: <REDACTED>' \
--header 'DD-APPLICATION-KEY: <REDACTED>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "timeboard for monitoring step",
    "is_read_only": false,
    "layout_type": "ordered",
    "reflow_type": "auto",
    "title": "madlee_vagrant_timeboard 5.0",
    "widgets": [
        {
            "definition": {
                "color": "green",
                "font_size": "18",
                "text": "my_metric text box",
                "text_align": "center",
                "type": "free_text"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q":"avg:my_metric{*}"
                    }
                ],
                "title": "My Custom Metric"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q":"sum:my_metric{*}.rollup(sum,3600)"
                    }
                ],
                "title": "My Custom Metric: Rolled Up to Past Hour (Historical)"
            }
        },
        {
            "definition": {
                "type": "query_value",
                "requests": [
                    {
                        "q":"sum:my_metric{*}.rollup(sum,3600)"
                    }
                ],
                "title": "My Custom Metric: Rolled Up to Past Hour"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q":"anomalies(avg:my_metric{*}, '\''basic'\'',3)"
                    }
                ],
                "title": "My Metric (test): Anomaly Detection"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q":"anomalies(sum:postgresql.commits{*}, '\''basic'\'',3)"
                    }
                ],
                "title": "My Postgres Commits Metric: Anomaly Detection"
            }
        }
    ]
}'
```

After setting the dashboard to the past 15 minutes, tagging myself and sending myself the screenshot - see below.

![last_15](https://user-images.githubusercontent.com/20326531/124520047-14e52700-dda0-11eb-9110-80ceb9a6cbbb.png)

Note that when filtered to the last 5 minutes, my dashboard showed blank data - so did the actual metric in the Metrics section. However, It was collecting data as i ran a status command and saw the metric was collecting data. I also saw historical data continuously streaming on the metric value after - I am guessing there is around a 5 minute delay between the agent and the site but I was not able to find any documentation about modifying this.

## Monitoring Data

### Alert Email
![alert](https://user-images.githubusercontent.com/20326531/124517554-1d862f00-dd99-11eb-82f7-fcddf76387c1.png)

### Warning Email
![warning_email](https://user-images.githubusercontent.com/20326531/124517349-9e90f680-dd98-11eb-806d-c4e01ad448c1.png)

### No Data Email
![nodata](https://user-images.githubusercontent.com/20326531/124517526-08110500-dd99-11eb-8f69-17539cee3715.png)

### Scheduled Downtime Email (weekends)
![scheduled_downtime](https://user-images.githubusercontent.com/20326531/124517488-ef085400-dd98-11eb-891f-7bf75860ad51.png)


## Collecting APM Data

I used the flask app provided.
Then, I installed ddtrace and flask packages on my vagrant box.

Then, I put the ddtrace package inside the python script and ran the script referencing the [ddtrace docs](https://ddtrace.readthedocs.io/en/stable/integrations.html#flask)

![flask_app](https://user-images.githubusercontent.com/20326531/124517604-3e4e8480-dd99-11eb-98c9-a4e37a1b3931.png)

I populated the app with traffic.

```
curl "http://10.0.2.15:5050"
curl "http://10.0.2.15:5050/api/apm"
curl "http://10.0.2.15:5050/api/trace/"
```

I also used a python script to populate the app with traffic. see below:

```
import time
import random
import requests

def hit_flask(n):
   counter = 0
   while counter < n:
      requests('http://10.0.2.15:5050')
      time.sleep(random.randint(0,5))
      requests('http://10.0.2.15:5050/api/trace')
      requests('http://10.0.2.15:5050/api/apm')
      time.sleep(random.randint(0,15))
      counter = counter+1

if __name__ == '__main__':
    n=100
    hit_flask(n)

```

See screenshots of the Dashboard with APM and Infrastructure Metrics below:

link: https://p.datadoghq.com/sb/d20d36ac-dbba-11eb-ad10-da7ad0900002-a7343ff6404fbb56329e041cfc4b45c0

![APM_dash](https://user-images.githubusercontent.com/20326531/124521454-61cafc80-dda4-11eb-9f70-d494a0ff525a.png)


## Final Question

When thinking about creative ways to use Datadog, I started to ask myself a series of questions that would help me determine if I could even put information into the datadog cloud servers. These questions are listed below (not in order, not all required):

- What are processes with bottlenecks?
- What has uptime and downtime? E.g. can it be turned on and off?
- What can be managed remotely?
- What is time consuming to manage?
- What is taking in data? How is that data being stored? (can it be integrated easily with a datadog integration?)
- What has a server?
- What has an API?
- Are there 2 services that go together that are hard to manage separately?

These questions helped me create a long list, and then a short list, but the lowest hanging fruit that I found was to use Datadog for 3D printing monitoring. In college, I worked at our school library's MakerHub - a creative space designed for tinkering on all sorts of side projects. We had bookbinding stations, sewing and embroidery stations, a woodshop, a laser printer, sautering/electrical engineering station, and lastly, a 3D printing station. All of the stations had volunteers keeping eyes on members using the stations during open hours. However, the 3D printing station was a bit different. We would allow MakerHub members to sign up to use the 3D printer through our scheduling system. Then, they would estimate the time it would take to print their object. We would let them set it up, run it, and grab the print when they were done. However, this wasn't always a smooth process. In fact, our 3D printers were wildly unreliable. They were constatnly broken in multiple different ways. Prints could fail due to a number of reasons:

- wrong extrusion rate
- faulty design (structurally) through support beds or density of print
- extruder is actually broken!
- not enough filament/broken filament
- nozzle calibrated incorrectly
- print bed adhesion not strong enough

However, because these prints took such a long time (often overnight), volunteers and MakerHub Members would often leave the Makerhub once the print started, and come back when it was scheduled to be finished. Volunteers would often leave the 3D printing machine to finish overnight. Because of the fail rate, this led to a huge bottleneck in the amount of time it would take to get your print. If a print failed, a member was allowed to re-start it before the next person could start their print.

Datadog would alleviate this bottleneck by grabbing data from the 3D printer APIs. This would allow members and volunteers to have 24/7 view of the printers and what they are printing, if there were issues with the print, or even if the entire 3D printer was unavailable while it was being fixed. Instead of coming back the next morning to pick up a print only to see that it had failed halfway through, Datadog would monitor the uptime and downtime of a print, of a printer, see extrusion errors of fail errors for halfway through the print, etc. Volunteers and members would then triage the problem, and if it made sense to restart the print, go back to the library and restart it. I can see volunteers using a dashboard to determine that since a printer had failed most times over the past year during larger prints, it should be reserved for small prints only. Other pattern recognition on the overall heatlh of the machine would take place. This would save a lot of wasted time and allow prints to finish with on average, a smaller delay than without Datadog. 
  
