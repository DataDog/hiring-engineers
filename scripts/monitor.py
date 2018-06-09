from datadog import initialize, api
from datadog.api.constants import CheckStatus

options = {'api_key': 'caecf54c05497610bd221b11423fbf1d',
           'app_key': '505f3113a164f647a92a5bf6ced19c746677c118'}

initialize(**options)

options = {
    "notify_no_data": True,
    "no_data_timeframe": 10
}
tags = ["app:webserver", "frontend"]
api.Monitor.create(
    type="metric alert",
    query="avg:my_metric{*}",
    name="Bytes received on host0",
    message="We may need to add web hosts if this is consistently high.",
    tags=tags,
    options=options
)
