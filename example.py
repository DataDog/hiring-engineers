import os
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import dashboards_api
from datadog_api_client.v1.models import *
from pprint import pprint
# See configuration.py for a list of all supported configuration parameters.
configuration = Configuration()

# Enter a context with an instance of the API client
with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    body = Dashboard(

        layout_type=DashboardLayoutType("ordered"),
        title="SE Hiring Exercise Dashboard",
        widgets=[
            Widget(
                definition=WidgetDefinition(
                    requests=[{"q":"my_metric{host:zacserver}"}],
                    type="timeseries",
                    title= "My Metric Hourly",
                ),
                id=1,
                layout=WidgetLayout(
                    height=3,
                    is_column_break=True,
                    width=3,
                    x=1,
                    y=1,
                ),
            ),
            Widget(
                definition=WidgetDefinition(
                    requests=[{"q": "anomalies(avg:mysql.performance.user_time{host:zacserver},'basic',2)"}],
                    type="timeseries",
                    title= "MySQL CPU Anomalies",
                ),
                id=2,
                layout=WidgetLayout(
                    height=3,
                    is_column_break=False,
                    width=3,
                    x=5,
                    y=1,
                ),
            ),
            Widget(
                definition=WidgetDefinition(
                    requests=[{"q": "my_metric{host:zacserver}.rollup(sum, 3600)"}],
                    type="timeseries",
                    title= "My Metric Rollup",
                ),
                id=3,
                layout=WidgetLayout(
                    height=3,
                    is_column_break=False,
                    width=3,
                    x=1,
                    y=5,
                ),
            ),
        ],
    )  # Dashboard | Create a dashboard request body.

    # example passing only required values which don't have defaults set
    try:
        # Create a new dashboard
        api_response = api_instance.create_dashboard(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DashboardsApi->create_dashboard: %s\n" % e)
