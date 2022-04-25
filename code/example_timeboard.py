"""
Create a new dashboard returns "OK" response
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
    title="Timeboard Example",
    widgets=[
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Test Metric",
                requests=[
                    TimeseriesWidgetRequest(
                        q= "avg:test_metric{*}"
                    ),
                ],
            ),
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Anomaly function for my test metric",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(avg:test_metric{*}, 'basic', 3)"
                    ),
               ],
            ),
        ),Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Anomaly function for mongodb",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(avg:mongodb.opcounters.commandps{*}, 'basic', 3)"
                    ),
                ],
            ),
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Rollup Function",
                requests=[
                    TimeseriesWidgetRequest(
                        q="test_metric{*}.rollup(sum,3600)"
                    ),
                ],
            ),
        ),
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)

