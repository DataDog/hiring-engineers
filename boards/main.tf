provider "datadog" {
  api_key = "${var.datadog_api_key}"
  app_key = "${var.datadog_app_key}"
  api_url = "${var.datadog_api_uri}"
}

# Create a new Datadog timeboard
resource "datadog_timeboard" "eks" {
  title       = "EKS Timeboard (created via Terraform)"
  description = "created using the Datadog provider in Terraform"
  read_only   = true

  graph {
    title = "My Metric on EKS worker nodes"
    viz   = "timeseries"

    request {
        q = "avg:mymetric{host:i-086dbf5cf103fec3c}, avg:mymetric{host:i-0d5672bad4f6c6443}"
        type = "line"
        style = {
            palette = "dog_classic"
            type = "solid"
            width = "normal"
            }
        }
    }
  graph {
    title = "My Metric Rollup"
    viz = "query_value"
    
    request {
        q = "avg:mymetric{*}.rollup(sum,3600)"
        aggregator = "avg"
        }
    precision = "*"
    }
  
  graph {
    title = "DynamoDB Items"
    viz = "timeseries"

    request {
        q = "anomalies(avg:aws.dynamodb.item_count{*}, 'basic', 2)"
        type = "line"
        style = {
            palette = "dog_classic"
            type = "solid"
            width = "normal"
            }
        }
    yaxis = {
        scale = "linear"
        min = "auto"
        max = "auto"
        includeZero = true
        label = ""
    }
  }
}

resource "datadog_monitor" "mymetric" {
  name               = "My Metric monitor"
  type               = "query alert"
  message            = "My Metric Monitor Message:\n\n{{#is_alert}}\nMonitor Alarm, Alert threshold\nCurrent value {{value}}\n{{/is_alert}}\n{{#is_warning}}\nMonitor Alarm, Warning threshold\nCurrent value {{value}}\n{{/is_warning}}\n\n{{#is_no_data}}\nMonitor Alarm, No Data received\nCurrent value {{value}}\n{{/is_no_data}}\n\n{{#is_recovery}} My Metric avg is recovered{{/is_recovery}}\n\nNotify:@affoliveira@gmail.com"


  query = "avg(last_5m):avg:mymetric{*} by {host} > 800"

  thresholds = {
    warning           = 500
    warning_recovery  = 499
    critical          = 800
    critical_recovery = 799
  }

  notify_no_data    = true
  no_data_timeframe = 10
  renotify_interval = 0
  new_host_delay = 300

  notify_audit = false
  timeout_h    = 0
  include_tags = true

  # ignore any changes in silenced value; using silenced is deprecated in favor of downtimes
  lifecycle {
    ignore_changes = [silenced]
  }

  tags = []
}

# Create a new daily 1700-0900 Datadog downtime for a specific monitor id
resource "datadog_downtime" "weekend_downtime" {
  scope = ["*"]
  start = 1583539200
  end   = 1583625600
  monitor_id = datadog_monitor.mymetric.id

  recurrence {
    type   = "weeks"
    week_days = ["Sat", "Sun"]
    period = 1
  }
  message = "Weekend Downtime Notify:@affoliveira@gmail.com"
}

resource "datadog_downtime" "weekday_downtime" {
  scope = ["*"]
  start = 1583348400
  end   = 1583398800
  monitor_id = datadog_monitor.mymetric.id

  recurrence {
    type   = "weeks"
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    period = 1
  }
  message = "Weekday Downtime Notify:@affoliveira@gmail.com"
}
