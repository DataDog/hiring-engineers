"""
Utilize the Datadog API to create a Timeboard that contains:

-Your custom metric scoped over your host.
-Any metric from the Integration on your Database with the anomaly function applied.
-Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
from datadog_api_client.v1.model.log_query_definition_group_by import LogQueryDefinitionGroupBy
from datadog_api_client.v1.model.log_query_definition_group_by_sort import LogQueryDefinitionGroupBySort
from datadog_api_client.v1.model.log_query_definition_search import LogQueryDefinitionSearch
from datadog_api_client.v1.model.logs_query_compute import LogsQueryCompute
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_sort import WidgetSort

body = Dashboard(
    layout_type=DashboardLayoutType("ordered"),
    title="Hiring Test Visualizing Data Maria",
    widgets=[
        # Average my metric
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="My Custom Metric",
                requests=[
                    TimeseriesWidgetRequest(
                        q="avg:my_metric{*}"
                    )
                ],
            )
        ),
        # Anomaly function
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Anomaly function for DB CPU performance",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"
                    )
                ],
            )
        ),
        # Rollup function
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Rollup function for my custom metric - Sum up all points for the past hour",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{*}.rollup(sum, 3600)"
                    )
                ],
            )
        ),
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)
