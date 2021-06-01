variable "datadog_api_key" {
  type = string
  description = "Datadog API Key"
}

variable "datadog_app_key" {
  type = string
  description = "Datadog Application Key"
}

provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
}

resource "datadog_dashboard" "cart_total_dashboard" {
  title         = "Cart Total"
  description   = "Automated with Terraform"
  layout_type   = "ordered"
  is_read_only  = true

 widget {
    timeseries_definition {
      request {
        q            = "anomalies(avg:cart.dollar_total{*}, 'basic', 2)"
        display_type = "line"
        style {
          palette    = "warm"
          line_type  = "solid"
          line_width = "normal"
        }
      }
    }
 }

  widget {
    check_status_definition {
      check = "datadog.agent.up"
      grouping = "check"
      group = "host:vagrant"
      title = "Host Availability (Vagrant)"
    }
  }

  widget {
    check_status_definition {
      check = "datadog.agent.up"
      grouping = "check"
      group = "host:docker"
      title = "Host Availability (Docker)"
    }
  }


}
