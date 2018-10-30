from datadog import initialize, api

# Set our api and app keys
# Note that if you accidentally type api-key instead of api_key
# you will lose 90 minutes and half your mind trying to figure
# out why the initialize call keeps failing. Ask me how I know.
options = {
   'api_key':'a4b4f014a70187b540f877a1faf71d67', 
   'app_key':'be34903eeacd6fb1da9756da7e62d2e4207c147f'
}


initialize(**options)

title = 'my_metric Timeboard'
description = 'Super Fantastic Timeboard for my_metric'
graphs = [{
   # Our first graph will be the average value of my_metric
   'definition': {
      'events': [],
      'requests': [
         {'q': 'avg:my_metric{*} by {hosts}'}
      ],
      'viz': 'timeseries'
   },
   'title': 'Average Value of my_metric by Host'
},
{
   # Our second graph will show the cpu usage of our mySQL database
   'definition': {
      'events': [],
      'requests': [
         {'q': "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
      ],
      'viz': 'timeseries'
   },
   'title': 'Anomalies in MySQL CPU Usage by Host'
},
{
   # Finally, let's add a query_value to our timeboard that shows the sum
   # of the my_metric values over the last hour.
   'definition': {
      'events': [],
      'requests': [
         {'q': 'avg:my_metric{*}.rollup(sum,3600)'}
      ],
      'viz': 'query_value',
      'status': 'done'
   },
   'title': 'Rollup of my_metric Over Last Hour'
}
]

# Set some basic variables for our timeboard
template_variables = [{
   'name': 'host1', 
   'prefix': 'host',
   'default': 'host:my-host'
}]

read_only=True

# Call the api to create the timeboard
api.Timeboard.create(
   title=title,
   description=description,
   graphs=graphs,
   template_variables=template_variables,
   read_only=read_only
)
