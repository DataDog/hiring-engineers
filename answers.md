# Martin Zerbib exercise

## The Datadog Agent
I initially installed the docker image of the agent but then chose to go for the Mac OS agent instead.
![Screenshot 2019-02-18 at 19.18.10.png](https://www.dropbox.com/s/i43pwqlq1uq3cmw/Screenshot%202019-02-18%20at%2019.18.10.png?dl=0&raw=1)

It ended up a good decision as I could use the taskbar to quickly restart as well as using the Web UI to debug certain checks and configs.

![Screenshot 2019-02-18 at 19.19.48.png](https://www.dropbox.com/s/naejjbhrauz4tw2/Screenshot%202019-02-18%20at%2019.19.48.png?dl=0&raw=1)


## Host & Tags

I set up tags for my host in the ```datadog.yaml``` file
![Screenshot 2019-02-18 at 22.52.59.png](https://www.dropbox.com/s/lkkazwfdokvz1xh/Screenshot%202019-02-18%20at%2022.52.59.png?dl=0&raw=1)

These tags appear in the host map.
![Screenshot 2019-02-18 at 20.46.40.png](https://www.dropbox.com/s/1dtetfj4ea72npm/Screenshot%202019-02-18%20at%2020.46.40.png?dl=0&raw=1)


## Custom Metric
To create a custom metric ranging between 0 and 1000 I first had to write a python script that would return a random number between 0 and 1000 and add that to the checks.d folder

**checks.d/assessmentcheck.py**
```python
try:    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck
import random

class AssessmentCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

Once that was done I needed to create the associated agent configuration for the check.
*Note that this step wasn't initially clear to me so it took me a few restarts of the agent to figure it out :)*

**conf.d/assessmentcheck.yaml**
```yaml
init_config:
instances:
  - min_collection_interval: 45
    [{}]
```
*Note: I didn't have the min_collection_interval initially but I noticed while doing the write up that one of the steps was to set the collection interval to 45 so I assume that is the correct setting*


## Setting up Mongo and Monitoring with Datadog

I installed MongoDB with HomeBrew
![Screenshot 2019-02-17 at 16.36.42.png](https://www.dropbox.com/s/gvp9vw9vll8v0w8/Screenshot%202019-02-17%20at%2016.36.42.png?dl=0&raw=1)

Added a datadog user...
![Screenshot 2019-02-17 at 16.35.43.png](https://www.dropbox.com/s/cd3csl32mmwoifw/Screenshot%202019-02-17%20at%2016.35.43.png?dl=0&raw=1)

...which I referenced in a configuration yaml file in the agent settings, before restarting the agent.

![Screenshot 2019-02-18 at 20.13.07.png](https://www.dropbox.com/s/6pi0ijwv99h8roi/Screenshot%202019-02-18%20at%2020.13.07.png?dl=0&raw=1)

The mongo I installed was completely unused and thus quite uninteresting to monitor, I did add some sample data and queried it to verify that data was showing up correctly.
I used the MongoDB default dashboard that appeared after enabling the integration but cloned it and converted some of the tiles to global time since they were all showing the last 4 hours by default and thus only showing data at the very tail of each graph.
*I had to convert each tile manually but I'm sure there's an easier way !*

![Screenshot 2019-02-17 at 16.14.45.png](https://www.dropbox.com/s/50gi5fncu05e6v7/Screenshot%202019-02-17%20at%2016.14.45.png?dl=0&raw=1)


## Dashboard 

[Dashboard Link](https://app.datadoghq.com/dashboard/9gy-54j-i7m/solutions-engineer-timeboard) -  Curious how this link would work since I couldn't find a way to share timeboards.

I did notice you could [create public urls on screenboards](https://p.datadoghq.com/sb/hlwz64novoda8pmk-85613198ec30dc28c8d51323d8cb1a39).

![Screenshot 2019-02-18 at 20.01.33.png](https://www.dropbox.com/s/3ksac607aklkp5k/Screenshot%202019-02-18%20at%2020.01.33.png?dl=0&raw=1)

Rather than using my uninteresting unused MongoDB I setup a monitor on my Chrome process so that the anomaly graph would be more interesting. The anomaly detection shows spikes in CPU usage for my Chrome process, i.e. whenever the deviation change of CPU usage exceeds the standard range.
![Screenshot 2019-02-18 at 20.14.35.png](https://www.dropbox.com/s/a2sovxox28y219e/Screenshot%202019-02-18%20at%2020.14.35.png?dl=0&raw=1)

I mentioned myself on the graph and got an email alert
![Screenshot 2019-02-18 at 20.09.16.png](https://www.dropbox.com/s/c0fupq2oijp5z4x/Screenshot%202019-02-18%20at%2020.09.16.png?dl=0&raw=1)![Screenshot 2019-02-18 at 20.09.36.png](https://www.dropbox.com/s/rzfl1t7km7ci78q/Screenshot%202019-02-18%20at%2020.09.36.png?dl=0&raw=1)

## Collecting Metrics



## Monitor 

**Creating a Monitor**
![Screenshot 2019-02-18 at 20.20.10.png](https://www.dropbox.com/s/w3goj9qkch3bx5y/Screenshot%202019-02-18%20at%2020.20.10.png?dl=0&raw=1)

**Setting it up and adding custom messages**
![Screenshot 2019-02-18 at 20.31.04.png](https://www.dropbox.com/s/ptei8yj4vxnp32q/Screenshot%202019-02-18%20at%2020.31.04.png?dl=0&raw=1)

**Receiving an Alert**


![Screenshot 2019-02-18 at 22.51.22.png](https://www.dropbox.com/s/ml9an081luzphdf/Screenshot%202019-02-18%20at%2022.51.22.png?dl=0&raw=1)
**Scheduling Downtime**

7PM to 9AM
![Screenshot 2019-02-18 at 20.32.31.png](https://www.dropbox.com/s/i7ckqm0js0lkliy/Screenshot%202019-02-18%20at%2020.32.31.png?dl=0&raw=1)

Weekend
![Screenshot 2019-02-18 at 20.36.11.png](https://www.dropbox.com/s/uy2syp4oxd3684e/Screenshot%202019-02-18%20at%2020.36.11.png?dl=0&raw=1)



## APM 

I left the flask app as is but leveraged the ddtrace python application which allowed me to run the flask app with automatic monitoring using the ddtrace-run command.

```pip install ddtrace```

![Screenshot 2019-02-18 at 19.05.34.png](https://www.dropbox.com/s/26hvwazjp5a6rkk/Screenshot%202019-02-18%20at%2019.05.34.png?dl=0&raw=1)

I had to enable APM monitoring so that my agent could receive the events sent over by ddtrace 
![Screenshot 2019-02-18 at 19.23.43.png](https://www.dropbox.com/s/t2w17iav8if3kdi/Screenshot%202019-02-18%20at%2019.23.43.png?dl=0&raw=1)

Uncommenting the right section wasn't enough though but after some github issues investigation on github of people reporting a similar issue on Mac I found that adding ```apm_enabled: true``` made it work.

The Flask Service showed up  in the APM section of Datadog.
![Screenshot 2019-02-18 at 19.42.53.png](https://www.dropbox.com/s/r3si1jgu9oml6cs/Screenshot%202019-02-18%20at%2019.42.53.png?dl=0&raw=1)

**Bonus Question -** A Service is a set of processes with a common overarching functionality, in the scope of this exercise we essentially encountered two services, a database service - mongodb and the flask web server. *I'll admit to a slight paraphrase of your docs there because once I read it to check my thoughts I couldn't think of a different way to say it :)*
A resource is an endpoint, a query, a request. Our flask app has mutliple resources that actually get listed in the resources section of the dashboard, such as /api/trace ,/api/apm or the root resource /.


**Final Question:** 
I've always had an interest in IOT, connected/smart devices. I think Datadog would be an awesome way to monitor many devices by implementing agents into each device or by implementing collection functionality into the phone apps which are used to control them on their local networks.

Monitoring of such devices could answer usecases such as predictive maintenance ( predicting when a device will fail ), improved support, more accurate troubleshooting, cost reduction by fixing only the faulty parts etc.

