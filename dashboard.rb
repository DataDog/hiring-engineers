# Create a new dashboard returns "OK" response

require "datadog_api_client"

api_instance = DatadogAPIClient::V1::DashboardsAPI.new

body = DatadogAPIClient::V1::Dashboard.new({
  layout_type: DatadogAPIClient::V1::DashboardLayoutType::ORDERED,
  title: "Datadog SE Candidate Dashboard",
  widgets: [
    DatadogAPIClient::V1::Widget.new({
        definition: DatadogAPIClient::V1::QueryValueWidgetDefinition.new({
            type: DatadogAPIClient::V1::QueryValueWidgetDefinitionType::QUERY_VALUE,
            requests: [
                DatadogAPIClient::V1::QueryValueWidgetRequest.new({
                    profile_metrics_query: DatadogAPIClient::V1::FormulaAndFunctionMetricQueryDefinition.new({
                        aggregator: "avg",
                        data_source:"metrcis",
                        name: "query1",
                        query: "avg:my_metric(host:gavin-MacBookAir}"
                    })
                })
            ]
        })
    })
  ]
})
p api_instance.create_dashboard(body)