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
     title="Dashboard by API",
     widgets=[
         Widget(
             definition=TimeseriesWidgetDefinition(
                 type=TimeseriesWidgetDefinitionType("timeseries"),
                 title="Avg of My_Metric",
                 requests=[
                     TimeseriesWidgetRequest(
                         q="avg:my_metric{host:i-0e2dfdd13e28e8a1a}")
                         ],
                     )
                 ),
         Widget(
             definition=TimeseriesWidgetDefinition(
                 type=TimeseriesWidgetDefinitionType("timeseries"),
                 title="Database + Anomaly - Avg of PostgreSQL Connections",
                 requests=[
                     TimeseriesWidgetRequest(
                         q="anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"
                         )
                     ],
                 )
             ),
            Widget(
             definition=TimeseriesWidgetDefinition(
                 type=TimeseriesWidgetDefinitionType("timeseries"),
                 title="My_Metric with Rollup Function - Sum of All Points in Last Hour",
                 requests=[
                     TimeseriesWidgetRequest(
                         q="my_metric{host:i-0e2dfdd13e28e8a1a}.rollup(sum, 3600)"
                         )
                     ],
                 )
             )
     ]
 )


configuration = Configuration()

configuration.api_key["apiKeyAuth"] = "bad84019978135d6a4b7edcda743d85f"
configuration.api_key["appKeyAuth"] = "26f67d5f1daed82c3701cb3488b979e38cb2cbff"
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)
       
