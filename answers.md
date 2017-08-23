# QUESTIONS
1. The agent is data monitoring and collection software that runs in the background of a client's hosts. For whatever settings the client customizes it to monitor, the software collects data on these items and sends it to Datadog. Datadog then takes this data and creates graphical visualization and other data analytics tools.

2. A timeboard is shows all the dashboard graphs phased during the same time period in a grid display. This option is great for comparing and troubleshooting issues across multiple metrics. Also, each graph can be shared individually. A screenboard is the more customizable option for a high level review of metrics and are able to be viewed across different time frames. Screenboards can only be shared as a whole. It seems timeboards are better utilized when studying details and smaller troubleshooting system issues. Screenboards seem to be better utilized when presenting a high level view of metrics.



# IMAGES
![Adding tags to configuration file](img/01.png?raw=true)
1 - This screenshot shows where I added personalized tags to my agent in the Datadog configuration file.

![Host with customized tags](img/02.png?raw=true)
2 - My host (Macbook - local) with the customized tags in my Datadog dashboard.

![Update postgres config file to connect to Agent](img/03.png?raw=true)
3 - I decided to use PostgreSQL to host my database as I'm most familiar with it (I have experience with MYSQL also). Here I updated the postgresql yaml file with the generated username and password per the integration installation instructions. I named the database 'datadogdb'

![Check agent status to ensure postgresql check has passed](img/04.png?raw=true)
4 - Here I am showing my terminal where my postgresql integration check was passed. I split the screen to show my dashboard display of the host map. I am monitoring 2 hosts (home and local) on my macbook. The postgresql integration was added to my home host.

![Create test yaml file for check configuration](img/05.png?raw=true)
5 - I created a yaml configuration file here, with the required inputs but empty values, as directed for this type of simple check.

![Create method for gauge check at random sample numbers](img/06.png?raw=true)
6 - Here is the python file with the method for the random sample check. I defined the 'value' variable before the check method and passed it as a parameter.

![Cloned postgres dashboard](img/07.png?raw=true)
7 - I cloned the postgresql dashboard here.

![Cloned postgres dashboard with added metrics](img/07.png?raw=true)
8 - Here are a few of the metrics I added to the cloned dashboard. 
      - Random Sample Number Test as a timeseries graph
      - Hello World Example check as a query value graph
      - Average Serialization Status on a heat map

![Snapshot with notification being sent to my email](img/09.png?raw=true)
9 - Sending a snapshot of the random sample number graph to my email with a box drawn around where the metric is above 0.90.

![Random Sample Number test above 0.9 monitor](img/10.png?raw=true)
10 - Here is my monitor setup page for the random sample number test being above 0.90. I made the monitor a multi alert to prepare for an infrastructure growths. 

![Random Sample Number test above 0.9 monitor](img/11.png?raw=true)
11 - A continuation of my monitor setup page. Here I added a descriptive message and title with a notification to my email. I also linked the full cloned dashboard for the team being notified to access easier. 

![Random Sample Number monitor notification email](img/12.png?raw=true)
12 - Here is the monitor notification email for the random sample number metric (please excuse how ridiculously full my email inbox is lol)

![Random Sample Number monitor downtown setup](img/13.png?raw=true)
13 - I scheduled the downtime for the random number monitor for 7pm-9am here. 

![Random Sample Number downtime notification email](img/14.png?raw=true)
14 - Since it is after 7pm, my downtime won't go into affect until tomorrow at 7pm. In order to check for an email notification, I created a downtime at midnight since that's close to the time now. This shows where the scheduled downtime was activated.



# LINKS

## Home Host Dashboard:
https://app.datadoghq.com/dash/host/330764956?live=true&page=0&is_auto=false&from_ts=1503371943157&to_ts=1503375543157&tile_size=m

## Cloned Postgresql Dashboard:
https://app.datadoghq.com/dash/344868/postgres---overview-cloned?live=true&page=0&is_auto=false&from_ts=1503371850654&to_ts=1503375450654&tile_size=m

## Random Test Sample Check Metrics Graph:
https://app.datadoghq.com/dash/integration/custom%3Atest?live=true&page=0&is_auto=false&from_ts=1503371889554&to_ts=1503375489554&tile_size=m
