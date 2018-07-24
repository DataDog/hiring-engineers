provider "datadog" {}

resource "datadog_timeboard" "my_metric" {
  title       = "My Metric Timeboard"
  description = "created using the Datadog provider in Terraform"

  graph {
    title = "My Metric over ubuntu-xenial"
    viz   = "timeseries"

    request {
      q    = "avg:my_metric{host:ubuntu-xenial}"
      type = "line"
    }
  }

  graph {
    title  = "PostgreSQL commits with anomaly function"
    viz    = "timeseries"
    
    request {
      q    = "anomalies(avg:postgresql.commits{*}, 'basic', 2)"
      type = "line"
    }
  }

  graph {
    title  = "My Metric rolled up to 1 hr buckets"
    viz    = "timeseries"

    request {
      q    = "avg:my_metric{*}.rollup(sum, 3600)"
      type = "line"
    }
  }

}

resource "datadog_monitor" "my_metric" {
  name               = "My Metric Health"
  type               = "metric alert"
  message            = <<EOF
Notify: @elizondo_andre@live.com
{{#is_warning}} Your metric is in a warning state! {{/is_warning}}
{{#is_alert}} Your metric is alerting on Host IP: {{host.ip}} {{/is_alert}}
{{#is_no_data}} Looks like we're not getting any data! Fix it! {{/is_no_data}}
EOF

  query = "avg(last_5m):avg:my_metric{host:ubuntu-xenial} > 800"

  thresholds {
    warning           = 500
    critical          = 800
  }

  include_tags      = true
  notify_no_data    = true
  no_data_timeframe = 10 # how many minutes before calling no data

}

resource "datadog_downtime" "my_metric" {
  scope = ["host:ubuntu-xenial"]
  start = 1532397600
  end   = 1532448000

  recurrence {
    type   = "weeks"
    period = 1
    week_days = ["Mon","Tue","Wed","Thu","Fri"]
  }

  message = "@elizondo_andre@live.com A downtime has been scheduled!"

  monitor_id = "${datadog_monitor.my_metric.id}"
}

resource "datadog_downtime" "my_metric_weekend" {
  scope = ["host:ubuntu-xenial"]
  start = 1532761200
  end   = 1532934000

  recurrence {
    type   = "weeks"
    period = 1
    week_days = ["Sat","Sun"]
  }

  message = "@elizondo_andre@live.com A downtime has been scheduled!"
  
  monitor_id = "${datadog_monitor.my_metric.id}"
}