/* DataDog Monitor */

provider "datadog" {
  api_key = "${var.datadog_api_key}"
  app_key = "${var.datadog_app_key}"
}

resource "datadog_monitor" "demo-monitor" {
  name = "[${upper(var.environment)}] - Random Support Threshold exceeded"
  type = "metric alert"
  message = <<EOF
[${upper(var.environment)}] Random Support Threshold exceeded

[Code](https://github.com/random/somecode/blob/master/foo/bar.py)

[Logs](https://fakekibana.randomgenerator.io)

[Dashboard](https://app.datadoghq.com/screen/195008/mongodb----thematthewgreen)

[Runbook](https://fakewiki.randomgenerator.io)

{{#is_alert}}
The Random Support generator exceeds safe thresholds please investigate.
- Check Kibana for errors
- Check Sentry for errors
- Check DataDog dashboard for further insight
- Check Runbook for more detailed information
{{/is_alert}}
{{^is_alert}}
The Random Support generator load has returned to a reasonable level.
{{/is_alert}}
Notify: @thematthewgreen@gmail.com
EOF

  query = "avg(last_5m):avg:test.support.random{demo} by {host} > 0.9"
  thresholds {
    critical = 0.9
  }

  notify_no_data = false
  renotify_interval = 720

  notify_audit = false
  timeout_h = 0
  include_tags = true
}
