## Prerequisites - Setup the environment
* I chose to spin up a linux virtual machine on AWS: 

![alt text](https://i.imgur.com/m9SRJGL.png)

* I then installed the datadog agent and the host started to report metrics almost instantly.

![alt text](https://i.imgur.com/31wTzAz.png)

![alt text](https://i.imgur.com/340ZyDv.png)


## Collecting Metrics
* I added the tags to the configuration file: 
![alt text](https://i.imgur.com/v74Sy83.png)

* The host page showed the instance and the tags associated with it:
![alt text](https://i.imgur.com/9UshXO8.png)


* I went with installing MySQL: 
![alt text](https://i.imgur.com/btdrqau.png)

* Before I activated the integration I prepared the integration with DB access, rights, users etc.
![alt text](https://i.imgur.com/u0HPVEY.png)

* I then configured the integration on the agent and restarted it. 
![alt text](https://i.imgur.com/N9mWvIT.png)


* The integration was successful: 

![alt text](https://i.imgur.com/NlbzRJi.png)

* Data started to display on the dashboard:

![alt text](https://i.imgur.com/R9W0QnL.png)

* Below is the code for my Custom Agent Check
```
from checks import AgentCheck
from random import randint
class CustomAgentCheck(AgentCheck):
  def check(self, instance):
    randomvalue = randint(0, 1000)
    self.gauge('my_metric', randomvalue)
```    

* I changed the interval to 45 sec by adding min_collection_interval to the checks .yaml file.
``` 
init_config:
    min_collection_interval: 45

instances:
  [{}]
  ``` 
* **Bonus Question**:
You can change the interval by adding the min_collection_interval paremeter to the integrations YAML configuration. It's important to note that the agent has it's own interval configured as well.

## Visualizing Data:

* My timeboard showing infrastructure and integration (MySQL) metrics: 
![alt text](https://i.imgur.com/y0JDapB.png)

* A snapshot generated from one of the graphs: 
![alt text](https://i.imgur.com/rLjAHF5.png)

* **Bonus Question**:
The anomaly graph is displaying anomalies in the time series data, i.e identifying when a data point is deviating from the past normal behavior.

## Monitoring Data


* I added a monitor to alert on thresholds and send me an email if it occurs: 

![alt text](https://i.imgur.com/Geqfvl4.png)
![alt text](https://i.imgur.com/2m8y6Xl.png)

* Warning Email: ![alt text](https://i.imgur.com/w4HTtV4.png)
* Alert Email: ![alt text](https://i.imgur.com/jORA11p.png)

* **Bonus Question**: 

* Scheduled downtimes daily M-F 7PM to 9AM CEST (UAT in the screenshot): 
![alt text](https://i.imgur.com/pKQ9uKX.png)

* Sat-Sun all day: 
![alt text](https://i.imgur.com/6zRRj4O.png)

## Collecting APM Data:

* Instrumenting the flask application after installing the necessary dependencies: 
![alt text](https://i.imgur.com/o6DlrsT.png)

* A link and a screenshot of a Dashboard with both APM and Infrastructure Metrics: 
![alt text](https://i.imgur.com/rA9dccN.png)
    
* **Bonus Question**: 
A service is a collection of various processes to provide a certain feature, for instance a web application. The application can then consist of different services, for example a web app service or a database service.
A resource is a particular transaction or query to a service, for example an HTTP request or a SQL query.


## Final Question:

An interesting and creative way I would use datadog for is synthetic browser monitoring. It's a technique for monitoring the performance and end user experience of web applications.
These are the steps I would take to achieve this:
1. Spin up a VM or several VM's from different locations. 
2. Install the Datadog Agent and dependencies such as Selenium (emulate a browser client) and XVFB (virtual frame buffer since the VM doesn't have a GUI).
3. Write a python check that uses Selenium to browse a web page, execute a Javascript to fetch Performance data from the Navigation Timing API.
4. Emit the collected data to datadog.

Other interesting and creative use cases would be Business Intelligence. Writing integrations to collect data from various non-tech related sources like twitter or facebook, and correlate likes/dislikes with application performance.
