from datadog import initialize, api

options = {
    'api_key': '***REMOVED***',
    'app_key': '***REMOVED***'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:random.number{*}",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            },
            {
                "q": "avg:random.number{*}.rollup(sum, 300)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "viz": "timeseries"
    },
    "title": "Random Number Metrics"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:postgresql.db.count{*}, 'basic', 2)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "viz": "timeseries"
    },
    "title": "Database connections anomalies"
}]

read_only = True
result = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

print(result)