# DataDog Q&A

Hello, this is my journey through the technical test for the Solutions Engineer role at DataDog, Paris. I have included code snippets, images and links to support my answers. I have also made a note of hurdles I encountered and how I overcame them throughout my journey. While testing my technical abilities, the exercise also taught me a lot about the DataDog service, which I am sure will come in handy in my future. Thank you for the opportunity to learn!

## Pre-requisites: The Setup 

As recommended I installed Vagrant and VirtualBox to run Ubuntu v.16.04. To achieve this, the **Vagarantfile** needed to be modified to reflect the correct version required for the setup. After installing the DataDog agent, the environment was ready for the exercise.

## Collecting Metrics

This first section gave me a good insight into a datadog agent's role and the foundations of how the agent interfaces with systems to collect data.

- **Tags**: 

  When there is a multitude of applications and systems across an infrastructure, tags help keeping relevant pieces grouped together for easy identification. Tags can be added through the Agent config file located inside the installed datadog-agent folder. After identifying the agent config file's location (/etc/datadog-agent/datadog.yaml) on the Vagrant machine, I modified the .yaml file to add tags. The tags can be viewed from the Host Map on the DataDog UI.

  > Hurdle:
  >
  > Restarting the agent with `systemctl restart datadog-agent` should have updated the tags on the Host Map. But even after a few tries it did not seem to update. I ran `datadog-agent status` to check for problems:
  >
  > ![Screen Shot 2019-01-24 at 12.01.35 PM](/Users/rmshree/hiring-engineers/imgs/1.png)
  >
  > As suspected the permissions for the datadog-agent folder was not set for access. I changed the permissions and restarted the agent to find the updated Host Map with the tags I added.
  >
  > The final Host M

  ![](/Users/rmshree/hiring-engineers/imgs/2.png)

- **Postgres**: 

  The next step was connecting to a database. Since I've had experience using Postgres, I went ahead and installed it on the vagrant machine. I created a user with password according to the DataDog x Postgres docs and granted access to the user to collect and report the metrics.

  After finishing all the steps in the setup and restarting the agent, Postgres metrics were visible in the [dashboard](https://app.datadoghq.com/dash/integration/17/postgres---metrics?tile_size=m&page=0&is_auto=false&from_ts=1548356340000&to_ts=1548359940000&live=true&tv_mode=false) as well as through the Host Map:

  ![Screen Shot 2019-01-29 at 9.14.48 PM](/Users/rmshree/hiring-engineers/imgs/3.png)

- **Custom Agent**: 

  In order to create a custom agent check, I followed the [documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) and created a ***my_metrics.yaml*** file in `/etc/datadog-agent/conf.d` and ***my_metrics.py*** file in `/etc/datadog-agent/checks.d`. It is important to note that both files have to be of the same name, only with different extensions. 

  After restarting the agent and doing a status check showed the "my_metrics" info under Collectors. 

  ![Screen Shot 2019-01-25 at 10.19.51 AM](/Users/rmshree/hiring-engineers/imgs/4.png)Another way I made sure the custom metric was collecting metrics was by running `sudo -u dd-agent -- datadog-agent check my_metric`. It was also visible on the Host Map:

  ![Screen Shot 2019-01-25 at 10.52.55 AM](/Users/rmshree/hiring-engineers/imgs/5.png)



​	I then changed the file *my_metric.yaml* to have an instance parameter for interval set to 45. This modifies the collection of metrics to occur in intervals of 45 seconds instead of the default 15 seconds.

![Screen Shot 2019-01-25 at 10.48.05 AM](/Users/rmshree/hiring-engineers/imgs/6.png)

 

**Bonus**: For the previous part of this exercise, the interval was indeed changed through the yaml file and not the python file. I was interested in seeing how to do it from the python file in reverse but couldn't find anything on the surface through the documentation - seems like changing the yaml file is the most common method to go about modifying the interval.



## **Visualizing Data**

This section of the exercise really brought forward the dashboard functionalities of DataDog that can be applied to innumerable use cases. Having worked with BI tools, I understand the importance of a well-visualized dashboard and the impact it can have on high-level business decisions while also keeping track of performance indicators on a day-to-day basis. DataDog allows a mix and match of different metrics and events across an infrastructure to be visible on a single interactive dashboard that allows stakeholders to evaluate and share relevantly.

- **Timeboard**:

  In order to use the API for creating a Timeboard, I used curl from my vagrant machine’s terminal. Thanks to the [docs](https://docs.datadoghq.com/api/?lang=python#timeboards), the sample request provided only needed to be changed to reflect my api and app keys, and 'my_metric'. I could immediately see a new [dashboard](https://app.datadoghq.com/dash/1057532/my-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1548433380000&to_ts=1548436980000&live=true) for the custom metric on the UI. 

  I added another graph and used the [Postgres docs](https://docs.datadoghq.com/integrations/postgres/) to identify a metric to monitor and display using the anomaly function. I used the postgresql.bgwriter.buffers_alloc to monitor the number of buffers allocated to the database.

  The third graph was to display the rollup function applied to 'my_metric' to sum up all the points for the last hour into a single bucket. Because the rollup function takes method and time in seconds as arguments, I called the function with "sum" as the method and "3600" seconds as the time argument.

  The [Timeboard](https://app.datadoghq.com/dash/1061293/custom-metric-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1548812438933&to_ts=1548814164000&live=false) with these three graphs finally looked like this:

  ![Screen Shot 2019-01-29 at 9.09.13 PM](/Users/rmshree/hiring-engineers/imgs/7.png)



 

> Hurdle:
>
> I started off using Python for this section of the exercise. The python file with the API request worked until the second graph with the anomaly function but refused to run for the third graph. After spending some time trying to figure out what was wrong with my program, I checked the docs to find alternate ways so to check if the logic for my graphs are correct. Using curl from my terminal immediately to generate the new Timeboard with all the graphs, establishing that my logic was indeed correct. I abandoned the python program and went with curl to generate the final Timeboard.
>
> ​	![Screen Shot 2019-01-25 at 3.52.07 PM](/Users/rmshree/hiring-engineers/imgs/8.png)

  

The curl script I used to generate the new Timeboard with all the graphs for this section is below:

`curl -X POST 'https://api.datadoghq.com/api/v1/dash?api_key=dae7275d9faed4e6306cafaaaca7c57d&application_key=ea1c6d6d1ee0f2d3baea9bef74e9c66484f1fc09' -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d '{"graphs" : [{"title": "My Metric","definition": {"events": [],"requests": [{"q": "my_metric{host:ubuntu-xenial}"}],"viz": "timeseries"}},{"title": "Anomalies PSQL","definition": {"events": [],"requests": [{"q": "anomalies(postgresql.bgwriter.buffers_alloc{*}, '\''basic'\'', 2)"}],"viz": "timeseries"}},{"title": "Metric RollUp","definition": {"events": [],"requests": [{"q": "avg:my_metric{*}.rollup(sum, 3600)"}],"viz": "query_value"}}],"title" : "Custom Metric Timeboard","description" : "Interview for SE","template_variables": [{"name": "host1","prefix": "host","default": "host:my-host"}],"read_only": "True"}'`



​	In order to see metrics for a specific period of time, the interactive graphs allow you to select the timeframe by selecting and dragging over the graph. For modifying the timeframe, I dragged the mouse on the first graph to capture the last five minutes and it immediately zoomed in to display the 'my_metric' graph over that specific time:

![Screen Shot 2019-01-28 at 6.21.35 PM](/Users/rmshree/hiring-engineers/imgs/9.png)

​	

​	I sent myself a snapshot of this graph and received this notification on my email:

​	![Screen Shot 2019-01-25 at 4.18.09 PM](/Users/rmshree/hiring-engineers/imgs/10.png)

​	 

​	This is a great way to share and bring to attention a specific moment in the graph during the metrics collection that is relevant to a certain stakeholder, instead of having to share an entire dashboard that might be too much information or irrelevant to share.

**Bonus**: Anomaly detection is used in cases where threshold based alerting can become difficult because of a multitude of variables affecting the pattern. The machine-learning backed auto-detection surfaces abnormal data that is reported beyond or below an expected standard set based on historical data.



## **Monitoring Data**

Metrics that can be easily monitored through thresholds can be set up to warn or alert when it drops or spikes. Setting up a metric monitor on DataDog showed me how flexible and hassle-free notification systems can be.

- **Metric Monitor**:

  I created a metric monitor through the GUI to watch the custom metric I created earlier. I modified it to alert if it goes above 800, warns if it goes above 500 and notify if there has been no data for over 10 minutes. In order to get notified when any of these thresholds get triggered, I set condition based messages that will get delivered to my email. These were the settings of the monitor:

  ![screencapture-app-datadoghq-monitors-2019-01-25-17_44_00](/Users/rmshree/hiring-engineers/imgs/11.png)

  

  This is the warning notification I received after setting up the trigger emails:

   	![Screen Shot 2019-01-25 at 6.52.45 PM](/Users/rmshree/hiring-engineers/imgs/12.png)

 

​	I also scheduled downtimes for the email notifications since these are notifications that will come in quite frequently. I set downtimes for Out of Office hours on the weekdays and scheduled for the weekend. This can be done through the ‘Manage Downtime’ tab under Monitors. I received email confirmations for the set downtimes:

![Screen Shot 2019-01-25 at 8.05.28 PM](/Users/rmshree/hiring-engineers/imgs/16.png)	![Screen Shot 2019-01-25 at 8.05.38 PM](/Users/rmshree/hiring-engineers/imgs/13.png)

## Collecting APM Data

Application Performance Management allows users to deconstruct and analyze the entire application stack for troubleshooting and performance indicators. It is especially useful when application tracing can be implemented across popular libraries in a matter of seconds using a single command. Seeing DataDog's APM in action with the sample application provided and at the speed in which it was able to collect metrics was a true example of the platform's power.

- **Flask App**:

  Since I frequently use Flask to build web apps, I installed Flask on the vagrant machine and then installed ddtrace. I utilized the provided sample application code and saved it as **app.py**. After that, I just needed to run dd-trace along with the app using `ddtrace-run python app.py` to start collecting the application's performance metrics. On a separate terminal, I kept hitting the app with curl requests and within a matter of seconds, the APM monitor was live on the UI.

  ![screencapture-app-datadoghq-apm-service-flask-flask-request-2019-01-27-12_20_58](/Users/rmshree/hiring-engineers/imgs/14.png)

- **Service vs Resource**:   

  If an application is the service that is instrumented by putting together defined processes, a request to the application is the resource which provides the information queried by the user. In the above implementation of the Flask App, the app is the service and the curl requests we used to hit the app is the resource. 

This is the dashboard I put together to view APM and Infrastructure metrics side by side: https://app.datadoghq.com/dash/1058350/flask-apm-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1548728820000&to_ts=1548732420000&live=true.

![Screen Shot 2019-01-28 at 10.29.37 PM](/Users/rmshree/hiring-engineers/imgs/15.png)

 

## **Final**

1. DataDog's data analytics platform not only gives users an insight into historical performance to understand patterns but also enables them to act instantly on rectifying a current situation - especially if it can be automated to act on triggers. An everyday application of DataDog's monitoring service could be to auto control a room's temperature based on its level of occupancy. The monitoring service can be used to record a room's temperature in short intervals to maintain a target comfortable temperature. If the occupancy in the room increases, the temperature rise will trigger alerts to a smart thermostat that auto adjusts the temperature, always maintaining it to the optimum degree. This not only makes sure that the occupants are comfortable at all times, but also saves on energy by not overspending on heating or cooling. 

2. Another everyday application of DataDog's monitoring service could be to detect the number of open parking spaces in public parking structures. Many a times, we have wandered into a parking lot, vulturing around in circles trying to hunt a car that might reverse out of a spot, only to find that 2 other cars are vying for the same spot because you all saw it at the same time.  Only if there had been a board displaying "5 spots left" at the entrance, everyone would've been on their way to claim one of the other open ones. This system is possible by implementing sensors that simply collect the number of entries and exits and sending it to DataDog. The result can be a display at the entrance which warns cars of the number of open slots available in the parking structure. This would save drivers tons of time and decrease aggression in mall garages by a tremendous amount.