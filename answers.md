## Collecting Metrics
1) Config of the agent : [datadog.conf](dd-agent/datadog.conf)

Screenshot of the tags : ![alt text](screenshots/tags.png "Tags")

2) MySQL Integration has been chosen and done.

Screenshot of the host map : ![alt text](screenshots/host_map_sql.png "Host Map")

3) Code of the configuration file : [YAML file](dd-agent/conf.d/my_check.yaml)
Code of the check file : [Python file](dd-agent/checks.d/my_check.py)

Screenshot of the metric informations : ![alt text](screenshots/my_metric_definition.png "my_metric")

4) I changed the [configuration](dd-agent/conf.d/my_check.yaml) of the check

BONUS) I didn't modify the python script to do so, I modified the config in the YAML file. This is the only way I know, for now.

## Visualizing Data
Python script to create/update a board : [update_board.py](./update_board.py)
JSON file for the board : [board.json](./board.json)

Screenshot of the Timeboard:
![alt text](screenshots/my_timeboard.png "my timeboard")
I didn't receive an email after my annotation. I tried several times and I even changed my email adress. No success. I screenshoted the event in the event list.

BONUS) The Anomaly Graph displays a line (or other visualization) which can take 2 colors, blue or red. If the color goes to red for a part of the graph, it means that the value went below or higher the "usual" trend calculated by the anomaly algorithm. https://docs.datadoghq.com/guides/anomalies/ 

