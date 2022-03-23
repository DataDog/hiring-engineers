# Create a new dashboard returns "OK" response

require "datadog_api_client"

api_instance = DatadogAPIClient::V1::DashboardsAPI.new

body = DatadogAPIClient::V1::Dashboard.new({
  layout_type: DatadogAPIClient::V1::DashboardLayoutType::ORDERED,
  title: "Datadog SE Candidate Dashboard",
  widgets: [
    DatadogAPIClient::V1::Widget.new({
        definition: DatadogAPIClient::V1::TimeseriesWidgetDefinition.new({
            type: DatadogAPIClient::V1::TimeseriesWidgetDefinitionType::TIMESERIES,
            requests: [
                DatadogAPIClient::V1::TimeseriesWidgetRequest.new({
                    q: "my_metric{host:gavin-MacBookAir}"
                })
            ],
            title:: "My Metric",
            show_legend: false,
            legend_size: 0
        })
    }),
    DatadogAPIClient::V1::Widget.new({
        definition: DatadogAPIClient::V1::TimeseriesWidgetDefinition.new({
            type: DatadogAPIClient::V1::TimeseriesWidgetDefinitionType::TIMESERIES,
            requests: [
                DatadogAPIClient::V1::TimeseriesWidgetRequest.new({
                    q: "sum:my_metric{host:gavin-MacBookAir}.rollup(sum,3600)",
                    metadata: [
                        {
                            expression: "sum:my_metric{host:gavin-MacBookAir}.rollup(sum,3600)",
                            alias_name: "my_metric_hourly_rollup"
                        }
                    ],
                    display_type: "line",
                    style: {
                        palette: "dog_classic",
                        line_type: "solid",
                        line_width: "normal"
                    }
                })
            ]
        })
    })
  ]
})
p api_instance.create_dashboard(body)

# formulas: [
#     DatadogAPIClient::V1::WidgetFormula.new({
#         formula: "query1"
#     })
# ],
# queries: [
#     DatadogAPIClient::V1::FormulaAndFunctionMetricQueryDefinition.new({
#         aggregator: "avg",
#         data_source:"metrics",
#         name: "query1",
#         query: "my_metric(host:gavin-MacBookAir}"
#     })
# ]
# })