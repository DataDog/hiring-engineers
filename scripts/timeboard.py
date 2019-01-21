from datadog import initialize, api

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}


initialize(**options)
# if running from monitored host would add socket.gethostname() function
host_name = 'datadog-host'

title = "Exercise Timeboard"
description = "This timeboard contains a rollup sum of queries, a custom metric over a host, and anomaly detect on postgres percentage of max connections in use"

graphs=[
    {
        "definition": {
            "requests": [
                {"q": "sum:my_metric{host:" + host_name + "}.rollup(sum,3600)"
                }
                        ],
            "viz" : "query_value"
                      },
        "title": "Rollup over last hour"
    },

    {
        "definition": {
            "requests": [
                {"q":"avg:my_metric{host:" + host_name + "}"
                }
                        ],
            "viz" : "timeseries"
                      },
        "title": "Custom Check over host"              
     },
       
     {
         "definition": {
             "requests": [
                 {"q": "anomalies(avg:postgresql.percent_usage_connections{host:"+host_name + "}, 'basic', 6)"
                 }
                                       
                         ],
            "viz" : "timeseries"
                       },
        "title": "Anomaly detection on percentage of max connections in use in postgres"
     }
 
]

read_only=True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
