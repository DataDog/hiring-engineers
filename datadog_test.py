from datadog import initialize, api

options = {
    'api_key': '17ffc3c363f80618ec95867b3aff81d7',
    'app_key': '15cf29907ce2c3e54c9ea6e14b363b4ba9dbc013'
}

initialize(**options)

title = "Christians API Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
                {
                    "q": "avg:fakemetric.hits{host:vagrant-ubuntu-precise-64}",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    }
                }
        ],
        "viz": "timeseries",
        "status": "done"
    },
    "title": "Fakemetric over host"
},{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:postgresql.commits{host:vagrant-ubuntu-precise-64}, 'basic', 2)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "viz": "timeseries",
        "status": "done"
    },
    "title": "Anomalies"
},{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:fakemetric.hits{host:vagrant-ubuntu-precise-64}.rollup(sum, 3600)",
                "aggregator": "sum",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "viz": "query_value",
        "precision": "*"
    },
    "title": "Sum bucket"
}]

template_variables = []

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
