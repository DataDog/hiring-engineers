## Collecting Metrics
1) Config of the agent : [datadog.conf](dd-agent/datadog.conf)

Screenshot of the tags : ![alt text](screenshots/tags.png "Tags")

2) MySQL Integration has been chosen and done.

Screenshot of the host map : ![alt text](screenshots/host_map_sql.png "Host Map")

3) Code of the configuration file : [YAML file](dd-agent/conf.d/my_check.yaml)
Code of the check file : [Python file](dd-agent/checks.d/my_check.py)

Screenshot of the metric informations : ![alt text](screenshots/my_metric_definition.png "my_metric")

4) I changed the [configuration](dd-agent/conf.d/my_check.yaml) of the check

5) I didn't modify the python script to do so, I modified the config in the YAML file. This is the only way I know, for now.
