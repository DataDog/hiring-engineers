from datadog import initialize, api

options = {
    'api_key': 'c248c6b5f698b169afc5b281a257180f',
    'app_key': '4534fd82e77e6cbe968ad712ae652e213d00577a'
}

initialize(**options)

# Create Dashboard for Timeboards to exist.
list_id = 4741
name = 'My DataDog Technical Challenge Dashboard'

api.DashboardList.update(list_id, name=name)

api.DashboardList.get(4741)

# Create a timeboard in the dashboard to put the 3 challenges

dashboards = [
    {
        "type": "custom_timeboard",
        "id": 5858
    }
]

api.DashboardList.add_items(list_id, dashboards=dashboards)

title = "My DataDog Technical Challenge Timeboard"
description = "3 technical challenge visuals."

graphs = [{
    
    # Challege 1: Your custom metric scoped over your host

    "definition": {
        "events": [],
        'requests': [{
        'q': 'max:my_metric{host:precise64}'}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric Visual"},
    
    # Challenge 2: Any metric from the Integration on your Database with  
    # the anomaly function applied. I chose the MySQL CPU performance.

    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(max:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL CPU With Anomalies"},
    
    # Challenge 3: Your custom metric with the rollup function applied 
    # to sum up all the points for the past hour into one bucket

    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{host:precise64}.rollup(sum)"}
        ],
        "viz": "timeseries"
    },
    # {graph_json=graph_json,
    # "timeframe" ="1_hour",
    # size="medium",
    # legend="no"},
    "title": "My Custom Metric With Rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:precise64"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)



# Start a new discussion.
# Include a handle like this
api.Comment.create(
    handle='nic@oboechick.com',
    message='Hello, this is working! 1'
)

# Or set it to None
# and the handle defaults
# to the owner of the application key
api.Comment.create(message='Hello, this is working! 2')

