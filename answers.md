Here is answer to the exercise of a solutions engineer from bamboottb.
As you promised, it was quite fun!  
  
## About my environment

#### I built a Ubuntu 18.04.1 VM on vSphere environment and configured Datadog agent on it.  
  * Hostname: bamboo01  
  * IP: 172.16.148.5  

I also configured the agent on my own MacBook and K8s environment, but I proceeded the exercise with bamboo01.  
　　
　　
## Collecting Metrics:

#### Added two tags to bamboo01 by modifying /etc/datadog-agent/datadog.yaml  
  * site:hama  
  * env:prod  


Inserted tag information in /etc/datadog-agent/datadog.yaml

```yaml
tags: site:hama, env:prod
```

Here is a screenshot of Bamboo01 in Infrastructure list and Host Map  

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen01.png" alt="screen01"></a>

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen02.png" alt="screen02"></a>
　　
　　
#### Installed MySQL on Bamboo01 and Datadog MySQL integration as you instructed on Integration menu.

1. Created "datadog" user on MySQL and granted privileges.  
2. Created /etc/datadog-agent/conf.d/mysql.yaml
```yaml
※あとでコピー
```
3. Restarted datadog-agent  
　　
　　
####  Created a custome Agent check "my_metric".

1. Created /etc/datadog-agent/checks.d/my_metric.py

```python
※あとでコピー
```

2. Created /etc/datadog-agent/conf.d/my_metric.yaml

```yaml
init_config:

instances:
    [{}]
```

3. Restarted datadog-agent

Changed my check's collection by modifying /etc/datadog-agent/conf.d/my_metric.yaml
```yaml
※あとでコピー
```
　　
　　
####  I could change the collection interval by modifying YAML file.   
　　
　　
## Visualizing Data:

#### Created a Timeboard from API.
It seems that I don't have permission to create Public URL for the Timeboard, so I give the private one.  
[Timeboard Link](https://app.datadoghq.com/dash/946439/timeboard-from-api-python)  

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen03.png" alt="screen03"></a>

The file I used to create the Timeboard is located in the same GitHub directory.  
[timeboard_nokey.py](https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/timeboard_nokey.py)  

(info)I tried to create the Timeboard by shell at first, but I had trouble to create a graph with anomaly function.

```shell
$ ./timeboard.sh 
{"errors": ["Error parsing query: unable to parse anomalies(avg:mysql.performance.user_time{*}, basic, 2): Rule 'scope_expr' didn't match at ', 2)' (line 1, column 52)."]}
```
I also located a .sh file which didn't work in the same directory.  
[timeboard_nokey.sh](https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/timeboard_nokey.sh)  

After that I created the python file which contains same API call as the shell file and it worked.  
I appreciate if you could check the problem.  
　　
　　
####  Set the Timeboard's timeframe to the past 5 minutes by dragging on the graph.
I couldn't select "The Past 5 minutes" from drop down menu, so I wonder if this is right answer.  

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen04.png" alt="screen04"></a>  
　　
　　
####  Took a snapshot of this graph and send it to myself.

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen05.png" alt="screen05"></a>    
　　
　　
####  Anomaly graph is displaying not only the metric and also a gray band which indicates the range of normal behavior based on the past metric.  
　　
　　
## Monitoring Data

####  Created a Metric Monitor that watches my_metric.  
[my_metric monitoring](https://app.datadoghq.com/monitors/6690151)

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen06.png" alt="screen06"></a>  
  
  
Defined messages as below,
```
This is the message from Datadog.

{{#is_alert}} 
my_metric of {{host.name}} is Alert status : {{value}} 
Host IP : {{host.ip}}
{{/is_alert}}

{{#is_warning}}
my_metric of {{host.name}} is Warning status : {{value}} 
{{/is_warning}} 

{{#is_no_data}}
my_metric of {{host.name}} has not been collected for 10 minutes.
{{/is_no_data}} 
```
  
  
####  Received different messages based on Monitor status.

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen07.png" alt="screen07"></a>

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen08.png" alt="screen08"></a>

(info)I received so many emails from Monitor, therefore I turned notification off at the moment.

####  Scheduled two downtimes
[weekday downtime](https://app.datadoghq.com/monitors#downtime?id=403538534)  
[weekend downtime](https://app.datadoghq.com/monitors#downtime?id=403322283)  

(info)I received the notification of scheduled downtime, but the time zone mentioned was UTC in the mail even though I scheduled in my time zone (JST).  
I think it should be fixed because customers would be confused.  

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen09.png" alt="screen09"></a>  

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen10.png" alt="screen10"></a>  

(info)I also found that once I mute the Monitor manually all downtimes related with the Monitor ware deleted even if the downtimes ware recurring. I think it might be unexpected behavior.  
  
  
## Collecting APM Data:

#### instrumented the Flask app you provided

1. Installed dd-trace Python library
```shell
$ pip install ddtrace
```

2. Modified Flask app by inserting the Middleware  
[my-flask-app.py](https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/my-flask-app.py)


#### I found that a Service is one Flask application, whereas a Resource is each routing within the application.

#### Created a Timeboard which includes
* Request counts per Resource
* Avarage of Request duration per Resource
* VM user CPU usage
* VM network transfer rate  
    
[APM and Infrastructure Timeboard](https://app.datadoghq.com/dash/946689/apm-and-infrastructure)

<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen11.png" alt="screen11"></a>  
  
  
## Final Question

I think Datadog has great potential for IoT way. In my case, I have elderly parents in a far away place. So if I collect their health metrics using biosensors, I would be able to visualize their health status and get alerts when it indicates abnormal value.


## Appendix

I did a brief comparison with Wavefront.  
Wavefront is a real-time analytics tool based on time series DB, similar to Datadog.  
  
Wavefront has a rich query language which would be better than Datadog.
<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen12.png" alt="screen12"></a>  
  
On the other hand, Wavefront has few metric visualize method and Datadog has better one.
<img src="https://github.com/bamboottb/hiring-engineers/blob/solutions-engineer/screen13.png" alt="screen13"></a>  
  
I guess that Datadog is a good tool for people who need to look at their environment status in a single pane of glass at first, and Wavefront is for people who know what they should monitor strongly.
