from datadog import initialize, api

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)