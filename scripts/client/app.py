from datadog import initialize, api # import our modules from data dog

# set our api and app keys so we can authorise with datadog
options = {
    'api_key': 'de80ad2a1bffe3273e4765ac1b8a85d7',
    'app_key': '490954065d91b99b46fc59efc4a748141fae365b'
}
# pass in our options dictionary object
initialize(**options)

# let's create our timeboard

title = 'My First Timeboard with an anomaly monitor, and rollup sum'
description = 'A Timeboard is a dashboard of graphs. These graphs enable you to visualise your data over some scope of time.'
graphs = [{
    'title': 'my_metric graph',
    'definition': {
        'requests': [
            {'q': 'avg:my_metric{host:ubuntu-xenial}'} # our custom metric's average on our host
        ],
        'viz': 'timeseries'
    },
},
{
    'title': 'rows inserted',
    'definition': {
        'requests': [
            {'q': 'anomalies(top(avg:postgresql.rows_inserted{host:ubuntu-xenial}, 10, \'mean\', \'desc\'), \'basic\', 2)'}
        ],
        'viz': 'timeseries'
    }
},
{
    'title': 'sum of my_metric over the past hour',
    'definition': {
        'requests': [
            {'q': 'avg:my_metric{host:ubuntu-xenial}.rollup(sum,3600)'}
        ],
        'viz': 'timeseries'
    }
}]

resp = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)

print resp # let's print our response
