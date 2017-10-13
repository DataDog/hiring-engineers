<h2>You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM. You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image</h2>

<h4>I chose to use debian which I ran from Oracle Virtual Box<h4/>
  br/>
<h2>Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog<h2/>
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Agent_Tag_Config.PNG?raw=true" />
<img src="https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Tags%20Host%20Map.PNG?raw=true" />
  br/>
<h2>Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?<h2/>

<h4>Yes you can configure the interval in the yaml file for your custom check or the datadog config file as well.<h4/>
br/>
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
 
 

