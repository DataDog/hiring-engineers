
resource "datadog_dashboard" "ordered_dashboard" {
  title         = "My Custom Dashboard"
  description   = "Created using the Datadog provider in Terraform"
  layout_type   = "ordered"
  is_read_only  = true

  # Custom metric scoped over 1 of my hosts
  widget {
    timeseries_definition {
      request {
        q= "avg:my_metric{host:node1.jonjozwiak.com}"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      title = "Avg of my_metric over host:node1.jonjozwiak.com"
      show_legend = false
      time = {
        live_span = "1d"
      }
      yaxis {
        scale = "linear"
        include_zero = true
        min = "auto"
        max = "auto"
      }
    }
  }

  # Metric from Database integration with anomoly function
  widget {
    timeseries_definition {
      request {
        q= "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      title = "Avg of mysql.net.connections with Anomolies"
      show_legend = false
      time = {
        live_span = "1d"
      }
      yaxis {
        scale = "linear"
        include_zero = true
        min = "auto"
        max = "auto"
      }
    }
  }

  # Anomoly Function over host CPU 
  ### I did this because the DB stats were VERY boring - no activity!
  widget {
    timeseries_definition {
      request {
        q= "anomalies(avg:system.cpu.user{host:node1.jonjozwiak.com}, 'basic', 4)"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      request {
        q= "anomalies(avg:system.cpu.user{host:node2.jonjozwiak.com}, 'basic', 4)"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      request {
        q= "anomalies(avg:system.cpu.user{host:node3.jonjozwiak.com}, 'basic', 4)"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      title = "Cluster Host CPU Usage with Anomoly Detection"
      show_legend = false
      time = {
        live_span = "1d"
      }
      yaxis {
        scale = "linear"
        include_zero = true
        min = "auto"
        max = "auto"
      }
    }
  }

  
  # Custom metric with rollup function applied to sum up all the points for the past hour
  widget {
    timeseries_definition {
      request {
        q= "avg:my_metric{host:node1.jonjozwiak.com}.rollup(sum, 3600)"
        display_type = "line"
        style {
          palette = "dog_classic"
          line_type = "solid"
          line_width = "normal"
        }
      }
      title = "Rollup my_metric for past hour over host:node1.jonjozwiak.com"
      show_legend = false
      time = {
        live_span = "1d"
      }
      yaxis {
        scale = "linear"
        include_zero = true
        min = "auto"
        max = "auto"
      }
    }
  }

}


