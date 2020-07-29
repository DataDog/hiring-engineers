provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
}

resource "datadog_dashboard" "ordered"  {
  title         = "Custom Metric Timeboard"
  description   = "My custom metric scoped over my host"
  layout_type   = "ordered"
  is_read_only  = true

  widget {
    query_value_definition {
      request {
        q = "sum:mc.my_metric{*}.rollup(sum, 3600)"
        aggregator = "avg"
        conditional_formats {
          comparator = ">"
          value = "100"
          palette = "green_on_white"
        }
      }
      autoscale = true
      precision = "2"
      text_align = "center"
      title = "The Sum of My Metric's Data Points Rolled up from the past Hour into One Bucket"
      time = {
        live_span = "5m"
      }
    }
  }
  
widget {
  timeseries_definition {
    request {
      q = "anomalies(avg:mc.my_metric{*}, 'basic', 2)"
      display_type = "line"
      style {
        palette = "cool"
        line_type = "solid"
        line_width = "normal" 
      }
    }
    marker {
      display_type = "error dashed"
      value = "y = 0"
      }
    title = "My  Metric  w/ Basic Anomaly Function"
    show_legend = false
    legend_size = "0"  
  }

} 

widget {
    timeseries_definition {
      request {
        q= "avg:mc.my_metric{*}.rollup(sum)"
        display_type = "line"
        style {
          palette = "purple"
          line_type = "solid"
          line_width = "thin"
        }
        metadata {
          expression = "avg:mc.my_metric{*}.rollup(sum)"
          alias_name = "My Metric Gauge" 
        }
      }
     
      marker {
        display_type = "error solid"
        label = "y = 800"
        value = "y = 800"
      }
      marker {
        display_type = "warning dashed"
        value = "501 < y < 799"
        label = " Waring Zone "
      }
       marker {
        display_type = "ok solid"
        value = "1 < y < 500"
        label = " The Good Range "
      }
      title = "Sweet Spot Metric Check"
      show_legend = false
      legend_size = "0"
      time = {
        live_span = "1h"
      }
      
      yaxis {
        min = 0
      }
    }  
}