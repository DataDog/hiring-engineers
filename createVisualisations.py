from datadog import initialize, api

options = {
    'api_key': '529a4968bc0c8d8310e3864b80b94656',
    'app_key': '65e77981582505401c45c67767dd8a5267b43ca8'
}

initialize(**options)

title = "My Timeboard"
description = "This is totally gonna show off my mad skillz."
graphs = [{
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{i-need:money}"}
                ],
                "viz": "timeseries"
            },
            "title": "Avg of my_metric over i-need:money"
          },
          {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:mysql.innodb.data_reads{*}"}
                ],
                "viz": "timeseries"
            },
            "title": "Avg of mysql.innodb.data_reads over all hosts"
          },
          {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{i-need:money}.rollup(sum, 3600)"}
                ],
                "viz": "timeseries"
            },
            "title": "Sum rollup of last hour of Avg of my_metric over i-need:money"
          }]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

# Create a new monitor
monitor_options = {
    "notify_no_data": False,
    "no_data_timeframe": 20
}
tags = ["database"]
api.Monitor.create(
    type="metric alert",
    query="avg(last_1h):anomalies(avg:mysql.innodb.data_reads{*}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1",
    name="MySql Reads on the only host we have",
    message="Just doing this as per instructed.",
    tags=tags,
    options=monitor_options
)