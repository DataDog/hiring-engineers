<h2>You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM. You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image</h2>

<h4>I chose to use debian which I ran from Oracle Virtual Box<h4/>
  <br/>
<h2>Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog<h2/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Agent_Tag_Config.PNG?raw=true" />
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Tags%20Host%20Map.PNG?raw=true" />
  <br/>
<h2>Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?<h2/>

<h4>Yes you can configure the interval in the yaml file for your custom check or the datadog config file as well.<h4/>
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric%20check%201.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric_yaml.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric_collection_interval.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric_py.PNG?raw=true" />
<br/>

<h2>Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?<h2/>

<h4>The anomaly graph displays a separate line compared to historical behaviour and indicates where it has deviated from that past behaviour<h4/>

<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Timeboard%20Options.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Timeboard%20Snapshot.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Timeboard%20graphs.PNG?raw=true" />
<br/>
 
 
<h2>Monitoring Data: When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:<h2/>
<br/>

<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Email%20Notification%20Monitor.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Managed_Downtime.PNG?raw=true" />
<br/>


<h2>Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:<h2/>

<h4>I was able to deploy the app and configure it for monitoring. However, after doing so I was was receiving the soccket error seen below then after restarting the agent I was able to resolve it, but then received a connection error I have not been able to resolve. <h4/>

<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Socket%20Error.PNG?raw=true" />
<br/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/APM%20Connection%20Error.PNG?raw=true" />
<br/>

<h2>Bonus Question: What is the difference between a Service and a Resource?<h2/>

<h4>Services are typically a collection of processes that are interconnected to achieve a specific function. While a resource typically calls upon services to achieve a function.<h4/>

<h2>Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?<h2/>
<h4>I think an interesting application of datadog could be in the industrial space. Monitoring of manufacturing hardware and optimization of interconnected machinery (a specific machine is overheating, or a specific plants output is less than anothers and being able to identify how and why) or perhaps in the utilities space. Being able to monitor water and power plants efficiencies and uptime and issues in real time to address root problems. <h4/>
