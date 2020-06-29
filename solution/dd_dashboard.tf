resource "datadog_dashboard" "ordered_dashboard" {
  title        = "Datadog Tutorial Dashboard"
  description  = "Created using the Datadog provider in Terraform"
  layout_type  = "ordered"
  is_read_only = false

  widget {
    timeseries_definition {
      title = "Random Number from ${var.dogname}"
      request {
        q            = "avg:my_metric.gauge{name:${var.dogname}}"
        display_type = "bars"
        style {
          palette    = "dog_classic"
        }
        metadata {
          expression = "avg:my_metric.gauge{name:${var.dogname}}"
          alias_name = "${var.dogname} Random Number"
        }
      }
    }
  }

  widget {
    timeseries_definition {
      title = "PostgreSQL % Max Connections on ${var.dogname}"
      request {
        q            = "anomalies(avg:postgresql.percent_usage_connections{name:${var.dogname}}, 'basic', 2)"
        display_type = "bars"
        style {
          palette    = "orange"
        }
        metadata {
          expression = "anomalies(avg:postgresql.percent_usage_connections{name:${var.dogname}}, 'basic', 2)"
          alias_name = "PostgreSQL % Max Connections"
        }
      }
    }
  }

  widget {
    query_value_definition {
      title = "Sum of Random Numbers - Past Hour"
      precision = 0
      autoscale = false
      time = {
        live_span  = "1h"
      }
      request {
        q          = "avg:my_metric.gauge{name:${var.dogname}}.rollup(sum, 3600)"
        aggregator = "sum"
      }
    }
  }
}