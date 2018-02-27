from datadog import initialize, api

options = { 'api_key' : '736b97f01509c71840ed1b7007c15c3d',
	'app_key' : 'ccefaa0962b4e69865dc4f172f8ed91c2881eb55'
}

initialize(**options)

#Create a new monitor
options = {
    'notify_no_data' : True,
    'no_data_timeframe' : 10,
    'thresholds' : {'critical' : 800 , 'warning' : 500},
    'renotify_interval' : 5,
    'escalation_message' : '@event-3ti8vwpk'
}
tags = ['app:webserver', 'frontend']
api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):my_metric{host:datadog}",
    name="avg metric alert 800 on datadaog",
    message="metric alert 800 on datadog.",
    tags=tags,
    options=options
)
options = {
    'notify_no_data' : True,
    'no_data_timeframe' : 10,
    'thresholds' : {'critical' : 4 , 'warning' : 2},
    'renotify_interval' : 5,
    'escalation_message' : '@event-3ti8vwpk'
}
tags = ['app:webserver', 'frontend']
api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):system.net.udp.in_datagrams{host:datadog}",
    name="avg sytem udp on host",
    message="avg alart system udp on datadog.",
    tags=tags,
    options=options
)

