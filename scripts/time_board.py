from datadog import initialize, api

options = {
    'api_key': '999671e91d68186b81c5bd8b0f9c8cea',
    'app_key': 'd26fcab204d70de1a12b53612bc39fd82553d2c2'
}

initialize(**options)

title = "George's TimeBoard"
description = "A TimeBoard for solutions engineers."
graphs = [{
    "title": "My_Metric",
    "definition": {
        "events": [],
        "requests": [{
            "q": "avg:my_metric{*}"
        }]
    },
    "viz": "timeseries"
}, {
    "title": "Anomolies Monitor for PostgresDB timed checkpoints",
    "definition": {
        "events": [],
        "requests": [{
            "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{role:database:postgresql}, 'basic', 2)"
        }]
    }
}, {
    "title": "my_metric rollup point sum",
    "definition": {
        "events": [],
        "requests": [{
            "q": "avg:my_metric{*}.rollup(sum, 3600)"
        }]
    }
}]

read_only = True

api.Timeboard.create(title=title,
        description=description,
        graphs=graphs,
        read_only=read_only)
