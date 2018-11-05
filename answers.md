Your answers to the questions go here.
# Solution Engineer Answers
# by John Meagher

### Prerequisites - Setup the environment

I started the project by spinning up a ubuntu 16.04 linux box using vagrant. The specific box that I used was "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box" which I found on vagrantbox.es. Originally I tried to create my own vm using virtualbox but I was having trouble with the datadog agent integration. Once I switched over to the vagrant box the datadog agent integration went smoothly. 

### Collecting Metrics

Once the datadog agent was running. I didnt realize that the agent config file was the /etc/datadog-agent/datadog.yaml file initially. I was able to add tags via the gui. While working on the APM section I realized where I was supposed to initially do the tags so I went back and changed them in the datadog.yaml file. 
![tagged host](https://github.com/jmeagheriv/hiring-engineers/blob/master/HostTagged.JPG)

I installed mongodb community edition using the instructions for ubuntu xenial 16.04 from [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/). I configured a datadog user based on the  integration for mongodb, configuration tab in the datadoghq. Upon restarting the agent, the mongodb metrics started to report in. [CheckConfig Output](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkconfig.txt)
![mongodb integration](https://github.com/jmeagheriv/hiring-engineers/blob/master/MongoDBIntegration.JPG)

To create my_metric I created a checkvalue.d directory in the /etc/datadog-agent/conf.d directory. This is where I created a checkvalue.yaml. I created the checkvalue.py in the /etc/datadog-agent/checks.d directory. I followed along with the instructions [here](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6) and changed the files to fit this metric.
[checkvalue.yaml](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkvalue.yaml)
[checkvalues.py](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkvalues.py)

Originally I had changed my python file to have a `sleep(45)` line but after researching to solve the bonus question I found the min_collection_interval would be better and changed the checkvalue.yaml file. 

### Visualizing Data

This was probably the hardest part of the project for me to wrap my head around. The documentation on the api has the outline I needed to use but the word snapshot in the documentation made me second guess that I was in the right place. When I think of snapshot, I think of a still image of the current state of the graphs and not a dashboard of updating metrics. I eventually looked back at the example and realized that I could use that to create the dashboard. There wasn't a dropdown option for less than 1 hour displayed of the metrics in the dashboard but you click and drag to change the timespan for the whole dashboard. This was touched on in the datadog101 youtube series in the [dashboards video](https://youtu.be/U5RmKDmGZM4)
I configured my anomaly graph to show current mongodb connections since there isn't anything being stored in the database the other things didn't seem to be as interesting to me. The graph will show if there are an unusual amount of connections. If I were to create a bunch of mongodb sessions concurrently and end them abruptly, the anomaly graph will color in that spike red. If I left those sessions running for a long time eventually the graph will normalize that number of connections and it will no longer be red. It uses the history of the metric to predict the future values. If the value is outside of the expected range it will color it red on the graph. 
[timeboard.py](https://github.com/jmeagheriv/hiring-engineers/blob/master/timeboard.py)
![metric](https://github.com/jmeagheriv/hiring-engineers/blob/master/Rollup.JPG)
![metric5m](https://github.com/jmeagheriv/hiring-engineers/blob/master/5m%20interval.JPG)
![metric snapshot](https://github.com/jmeagheriv/hiring-engineers/blob/master/MetricSnapshot.JPG)

### Monitoring Data

I have experience with creating monitors in Zabbix so this part was pretty straight forward and easier for me than I expected. Since it was all gui work here are all the screencaps. 
![MetricMonitor](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor.jpg)
![MetricMonitor2](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor2.JPG)
![monitor triggered email](https://github.com/jmeagheriv/hiring-engineers/blob/master/MonitorEmail.JPG)

#### Bonus!

![M-F](https://github.com/jmeagheriv/hiring-engineers/blob/master/M-F%20Downtime.JPG)
![Weekends](https://github.com/jmeagheriv/hiring-engineers/blob/master/Sat-Sun%20Downtime.JPG)

###




