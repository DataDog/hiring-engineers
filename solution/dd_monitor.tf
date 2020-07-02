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

  query = "avg(last_5m):avg:my_metric.gauge{*} by {host} > 800"

  thresholds = {
    warning           = 500
    critical          = 800
  }

  notify_no_data    = true
  no_data_timeframe = 10
  renotify_interval = 60
}

# Warning: If you run this *after* 7pm you'll get an error,
# due to the start_date being in the past.
resource "datadog_downtime" "weeknights" {
  scope = ["*"]
  start_date = "${formatdate("YYYY-MM-DD", timestamp())}T${var.weeknight_dt_start}:00${var.utc_offset}"
  end_date   = "${formatdate("YYYY-MM-DD", timeadd(timestamp(), "24h"))}T${var.weeknight_dt_end}:00${var.utc_offset}"
  monitor_id = datadog_monitor.high_random_number.id
  message    = "Weeknight downtime scheduled @${var.email}"

  # We include Sunday as a 'weeknight' so we don't wake up
  # the engineers at 2am on Monday morning...
  recurrence {
    type   = "weeks"
    week_days = ["Sun","Mon","Tue","Wed","Thu","Fri"]
    period = 1
  }
}

resource "datadog_downtime" "weekends" {
  scope = ["*"]
  start_date = "${formatdate("YYYY-MM-DD", timeadd(timestamp(), "24h"))}T00:00:00${var.utc_offset}"
  end_date   = "${formatdate("YYYY-MM-DD", timeadd(timestamp(), "48h"))}T00:00:00${var.utc_offset}"
  monitor_id = datadog_monitor.high_random_number.id
  message    = "Weekend downtime scheduled @${var.email}"

  recurrence {
    type   = "weeks"
    week_days = ["Sat","Sun"]
    period = 1
  }
}