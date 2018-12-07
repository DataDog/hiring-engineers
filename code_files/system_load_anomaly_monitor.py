from datadog import initialize, api

options = {
    'api_key': '3c658e247c0076099c7676f2d42460df',
    'app_key': '9afb3a081055cf3f3ef8a2d57d3ba9d0a9c72699'
}

initialize(**options)

api.Monitor.create(
    type="query alert",
    query="avg(last_5m):avg:system.load.15{host:william-Q325UA} < 0.1",
    name="Load of system.load.15",
    message="Load dropped below acceptable range"
)
