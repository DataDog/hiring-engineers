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
                    q: "avg:my_metric{host:gavin-MacBookAir}"
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
#         query: "avg:my_metric(host:gavin-MacBookAir}"
#     })
# ]
# })