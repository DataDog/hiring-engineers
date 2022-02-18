"""
DataDog homework dashboard script
"""
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_sort import WidgetSort
host="{host:devmachine}"
body = Dashboard(
    layout_type=DashboardLayoutType("ordered"),
    title="DataDog Sales Engineer Assignment Dashboard",
    widgets=[
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="My Metric Widget",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{}".format(host)
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="MongoDB connections available+anomalies",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(mongodb.connections.available{}, 'basic', 2)".format(host)
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="My Metric rollup sum for past 60 minutes",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{}.rollup(sum,3600)".format(host)
                        )
                ],
            )
        )
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)