"""
Hiring Exercise - Giada Valsecchi 
March 2022

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

Create a new dashboard returns "OK" response
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType

from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_layout import WidgetLayout
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_display_type import WidgetDisplayType
from datadog_api_client.v1.model.widget_line_type import WidgetLineType
from datadog_api_client.v1.model.widget_line_width import WidgetLineWidth
from datadog_api_client.v1.model.widget_request_style import WidgetRequestStyle
from datadog_api_client.v1.model.widget_marker import WidgetMarker
from datadog_api_client.v1.model.group_widget_definition_type import GroupWidgetDefinitionType
from datadog_api_client.v1.model.group_widget_definition import GroupWidgetDefinition

body = Dashboard(
    layout_type=DashboardLayoutType("ordered"),
    title="Giada@Hiring Exercise: API Timeboard",
    widgets=[
    
        Widget(
            definition=GroupWidgetDefinition(
            type=GroupWidgetDefinitionType("group"),
            title="Custom Metric group",
            show_title=True,
            title_align="center",
            background_color="purple",
            layout_type="ordered",
            widgets=[
            
            
            Widget(
                definition=TimeseriesWidgetDefinition(
                    type=TimeseriesWidgetDefinitionType("timeseries"),
                    title="Your custom metric scoped over your host",
                    #markers=WidgetMarker(label="max", value="1000", display_type="info dashed"),
                    show_legend=True, legend_layout="auto", legend_columns=["avg","min","max","value","sum"],
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:giada_custom.metric{host:v-giada-host-1}",
                            style=WidgetRequestStyle(
                                palette="classic", line_type=WidgetLineType("solid"), line_width=WidgetLineWidth("normal")
                            ),
                            display_type=WidgetDisplayType("bars"),
                        )
                    ],
       
                ),
            #   layout=WidgetLayout(x=2, y=0, width=4, height=2),
                
            ),
            
            Widget(
                definition=TimeseriesWidgetDefinition(
                    type=TimeseriesWidgetDefinitionType("timeseries"),
                    title="Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket",
                    #markers=WidgetMarker(label="max", value="1000", display_type="info dashed"),
                    show_legend=True, legend_layout="auto", legend_columns=["avg","min","max","value","sum"],
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:giada_custom.metric{host:v-giada-host-1}.rollup(sum, 3600)",
                            style=WidgetRequestStyle(
                                palette="cool", line_type=WidgetLineType("solid"), line_width=WidgetLineWidth("normal")
                            ),
                            display_type=WidgetDisplayType("bars"),
                        )
                    ],
                ),
            #  layout=WidgetLayout(x=2, y=0, width=4, height=2),
                
            ),
            ]
            )
        ),

        Widget(
            definition=GroupWidgetDefinition(
            type=GroupWidgetDefinitionType("group"),
            title="MySQL Integration group",
            show_title=True,
            title_align="center",
            background_color="pink",
            layout_type="ordered",
            widgets=[
            
        
            Widget(
                definition=TimeseriesWidgetDefinition(
                    type=TimeseriesWidgetDefinitionType("timeseries"),
                    title="Any metric from the Integration on your Database with the anomaly function applied",
                    #markers=WidgetMarker(label="max", value="1000", display_type="info dashed"),
                    show_legend=True, legend_layout="auto", legend_columns=["avg","min","max","value","sum"],
                    requests=[
                        TimeseriesWidgetRequest(
                            q="anomalies(max:mysql.performance.kernel_time{host:v-giada-host-1}, 'basic', 2)",
                            style=WidgetRequestStyle(
                                palette="classic", line_type=WidgetLineType("solid"), line_width=WidgetLineWidth("normal")
                            ),
                            display_type=WidgetDisplayType("line"),
                            )
                    ],
                ),
  #     out=WidgetLayout(x=2, y=0, width=4, height=2),
            ),
            ]
            )
        )    
       
    ],
)


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

print(response)