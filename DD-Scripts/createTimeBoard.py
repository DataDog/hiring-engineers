from datadog import initialize, api

options = {
    'api_key': '1563e17cc4550500b44bfb04c08b3d0f',
    'app_key': 'defcc5f9d217ba39fdbb2ef7e58fbfc7409ff4a8'
}

initialize(**options)

title = "Visualizing Data Timeboard 2"
description = "Visualizing Data Candidate excercise 2"

graphs = [{'definition': {'viz': 'timeseries', 'status': 'done', 'requests': [{'q': "anomalies(avg:mongodb.mem.virtual{*}, 'basic', 6)", 'aggregator': 'avg', 'style': {'width': 'normal', 'palette': 'dog_classic', 'type': 'solid'}, 'type': 'line', 'conditional_formats': []}], 'autoscale': True, 'xaxis': {}}, 'title': 'MogoDB virtual memory Anomaly Detection'}, {'definition': {'viz': 'timeseries', 'status': 'done', 'requests': [{'q': 'avg:my_metric{env:production}', 'aggregator': 'avg', 'style': {'width': 'normal', 'palette': 'dog_classic', 'type': 'solid'}, 'type': 'line', 'conditional_formats': []}], 'autoscale': True, 'xaxis': {}}, 'title': 'Avg of my_metric scoped to host'}, {'definition': {'viz': 'timeseries', 'status': 'done', 'requests': [{'q': 'my_metric{*}.rollup(sum, 3600)', 'aggregator': 'avg', 'style': {'width': 'normal', 'palette': 'dog_classic', 'type': 'solid'}, 'type': 'line', 'conditional_formats': []}], 'autoscale': True, 'xaxis': {}}, 'title': 'my_metrics Rollup function to sum up all data points for the last hour'}]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)
                     