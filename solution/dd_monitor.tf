# These random numbers are too high...
resource "datadog_monitor" "high_random_number" {
  name               = "Random Number Alert"
  type               = "metric alert"
  message            = <<-EOM
    {{#is_alert}}
    ALERT - Random number is {{value}} on {{host.ip}} @${var.email}
    {{/is_alert}}
    {{#is_warning}}
    WARNING - Random number is {{value}} on {{host.ip}} @${var.email}
    {{/is_warning}}
    {{#is_no_data}}
    NODATA - No data from {{host.ip}} @${var.email}
    {{/is_no_data}}
  EOM

  query = "avg(last_5m):avg:my_metric.gauge{*} > 800"

  thresholds = {
    warning           = 500
    critical          = 800
  }

  notify_no_data    = true
  no_data_timeframe = 10
  renotify_interval = 60
}

# Downtime so we don't get alerted evenings and weekends
resource "datadog_downtime" "weeknights" {
  scope = ["*"]
  start_date = "2020-06-30T19:00:00-05:00"
  end_date   = "2020-07-01T09:00:00-05:00"
  monitor_id = datadog_monitor.high_random_number.id
  message    = "Weeknight downtime scheduled @${var.email}"

  recurrence {
    type   = "days"
    period = 1
  }
}

resource "datadog_downtime" "weekends" {
  scope = ["*"]
  start_date = "2020-07-04T00:00:00-05:00"
  end_date   = "2020-07-05T00:00:00-05:00"
  monitor_id = datadog_monitor.high_random_number.id
  message    = "Weekend downtime scheduled @${var.email}"

  recurrence {
    type   = "days"
    week_days = ["Sat","Sun"]
    period = 1
  }
}