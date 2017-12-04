## Setup the Environment
I decided to start a Vagrant VM (ubuntu 12.04) on my linux machine to not mess with environment.

I used the simplest Vagrant file to begin as quickly as possible.

## Collecting Metrics

* **Tags set up in the Agent config**
Here is the configuration of my agent : [datadog.conf](dd-agent/datadog.conf)<br>
I added one tag to describe the environment (env:) and one to set the role (role:).

My tags are well shown on the host map as expected: ![alt text](screenshots/tags.png "Tags")

* **Database installation and integration set up**
I chose to install a MySQL DB.

The integration has been done and the "mysql" app can be seen on the host map for my host : ![alt text](screenshots/host_map_sql.png "Host Map")

* **Custom Agent check**
Creating a custom agent check means adding two new files to the host.

The first one is a YAML which describes the configuration of the custom check : [YAML file](dd-agent/conf.d/my_check.yaml)

The second one is a Python script which defines what the check sends : [Python file](dd-agent/checks.d/my_check.py)

After the integration, we can see that the new metric is well sent by the Agent in the "all metrics" pannel : ![alt text](screenshots/my_metric_definition.png "my_metric")

* **Check collection interval change**
I changed the [configuration](dd-agent/conf.d/my_check.yaml) of the check by adding :
"min_collection_interval: 45" to the "init_config" part.

* **BONUS QUESTION : Can you change the collection interval without modifying the Python check file you created?**

I didn't modify the python script to do so, I modified the config in the YAML file. This is the only way I know, for now.

## Visualizing Data
Python script to create/update a board : [update_board.py](./update_board.py)
JSON file for the board : [board.json](./board.json)

Screenshot of the Timeboard:
![alt text](screenshots/my_timeboard.png "my timeboard")
I didn't receive an email after my annotation. I tried several times and I even changed my email adress. No success. I screenshoted the event in the event list.
My timeboard big : ![alt text](screenshots/my_timeboard_big.png "my timeboard big")

BONUS) The Anomaly Graph displays a line (or other visualization) which can take 2 colors, blue or red. If the color goes to red for a part of the graph, it means that the value went below or higher the "usual" trend calculated by the anomaly algorithm. https://docs.datadoghq.com/guides/anomalies/ 

## Monitoring Data
Screenshot of the e-mail when I received a "Warning" notification :
![alt text](screenshots/email_my_monitor.png "warning notification")

Here is my configuration for my monitor :
![alt text](screenshots/my_monitor_conf.png "warning notification")

BONUS) Again, I did not receive an e-mail when I set the downtimes, which is weird.
Here is the view of both in the downtime pannel.

Weekly Downtime :
![alt text](screenshots/weekly_downtime.png "warning notification")

Week-end Downtime:
![alt text](screenshots/weekend_downtime.png "warning notification")

## Collecting APM Data
[Link to my Dashboard](https://p.datadoghq.com/sb/b1131d66e-41a43718b5)
Screenshot of my dashboard :
![alt text](screenshots/apm_infra_board.png "warning notification")

BONUS) Following the python doc (http://pypi.datadoghq.com/trace/docs/), a "service" is "the name of a set of processes that do the same job", for example, the name of your app.
A ressource is "a particular query to a service". For example, an endpoint or a sql query.

## Final Question
Following the idea of monitoring NYC Subway System, I would like to monitor the Paris "Velib" System (Bike Service).
Each of the "hub" would be viewed as a Host and we could couple this with a map of Paris. We could monitor the number of bikes in each Hub and set up alerts when there is none, or when the hub is full.
By doing this, we could identify which hubs tend to be more often empty and add extra bikes. We could also identify the peak hours and so on.
I know that the city of Paris is already exposing some datas but could be nice to implement the dd agent on each hub.
