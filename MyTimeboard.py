from datadog import initialize, api

options = {'api_key': 'c9ad1ab3ba229d022cc99af54d0d448f',
           'app_key': '27e3ef83a637cfdd9233001e6ae8d2bb18783a0b'}

initialize(**options)

title = "My Custom Timeboard"
description = "This is my custom Timeboard created from the API"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}by{host}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {
              "q": "mysql.performance.user_time{*}by{host}",
              "type": "line",
              "style": {
                "palette": "cool",
				"width": "normal",
                "type": "solid"
             }
          },
          {
            "q": "anomalies(mysql.performance.user_time{*}by{host}, 'basic', 2)",
            "type": "area",
            "style": {
               "palette": "dog classic",
               "type": "solid",
               "width": "normal"
          }
        }

       ],
	   "viz": "timeseries"
    },
     "title": "Database Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
          {
              "q": "my_metric{*}by{host}.rollup(sum,120)",
              "type": "bars",
              "style": {
                 "palette": "dog classic",
                 "type": "solid",
                 "width": "normal"
				}
        }
       ],
       "viz": "timeseries"
},
     "title": "Rollup Custom Metric"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
