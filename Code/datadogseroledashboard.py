from datadog import initialize, api

options = {'api_key': '2d48d77b05c92f4c724805f5c6055610',
           'app_key': '488f4966561b13f18ce101602d1444196f468917'}

initialize(**options)

title = "TimeBoard Dashboard - SE Role"
description = "Timeboard Creation for SE Role"

# The following represents Challenge 1 - use my cusotm metric

graphs = [{
    "definition": {
        "events": [],
        "requests": [
          {"q":"avg:my_metric{host:serole}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric on SE Role"
},
 # This is for Challenge 2 - Any metric from the Integration on your Database with the anomaly function applied. 
 # As I am running MySQL I am going to leverage CPU Performance as a test

    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(max:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MYSQL Server with CPU Anamalies"},

# And now for Challenge 3 - Here will rollup the points for the past hour for the custom metric

    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{host:serole}.rollup(sum)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric With Rollup to 1 hour"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

# Post a message so we know it works via the events page
api.Comment.create(message='Congrats - you have a new Dashboard')