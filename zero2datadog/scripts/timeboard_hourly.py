import requests

url = "https://api.datadoghq.com/api/v1/dashboard"

payload = "{\n  \"title\": \"Zero2Datadog Hourly Anomalies\",\n  \"description\": \"A custom agent check configured to submit a metric named `my_metric` with a random value between 0 and 1000.\",\n  \"widgets\": [\n\t{\n\t  \"definition\": {\n\t\t\"type\": \"timeseries\",\n\t\t\"requests\": [\n\t\t  {\n\t\t\t\"q\": \"my_metric{host:gearbox09.dev.controlplane.info}\"\n\t\t  }\n\t\t],\n\t\t\"title\": \"My Hourly Metric\",\n\t\t\"show_legend\": false,\n\t\t\"legend_size\": \"0\"\n\t  }\n\t},\n\t{\n\t  \"definition\": {\n\t\t\"type\": \"timeseries\",\n\t\t\"requests\": [\n\t\t  {\n\t\t\t\"q\": \"sum:my_metric{host:gearbox09.dev.controlplane.info}.rollup(sum, 60)\",\n\t\t\t\"metadata\": [\n\t\t\t  {\n\t\t\t\t\"expression\": \"sum:my_metric{host:gearbox09.dev.controlplane.info}.rollup(sum, 60)\",\n\t\t\t\t\"alias_name\": \"my_hour\"\n\t\t\t  }\n\t\t\t],\n\t\t\t\"display_type\": \"line\",\n\t\t\t\"style\": {\n\t\t\t  \"palette\": \"dog_classic\",\n\t\t\t  \"line_type\": \"solid\",\n\t\t\t  \"line_width\": \"normal\"\n\t\t\t}\n\t\t  }\n\t\t],\n\t\t\"yaxis\": {\n\t\t  \"label\": \"\",\n\t\t  \"scale\": \"linear\",\n\t\t  \"min\": \"auto\",\n\t\t  \"max\": \"auto\",\n\t\t  \"include_zero\": true\n\t\t},\n\t\t\"title\": \"My Hourly Rollup\",\n\t\t\"time\": {},\n\t\t\"show_legend\": false,\n\t\t\"legend_size\": \"0\"\n\t  }\n\t},\n\t{\n\t  \"definition\": {\n\t\t\"type\": \"timeseries\",\n\t\t\"requests\": [\n\t\t  {\n\t\t\t\"q\": \"anomalies(avg:mysql.performance.cpu_time{host:gearbox09.dev.controlplane.info}, 'basic', 2)\",\n\t\t\t\"display_type\": \"line\",\n\t\t\t\"style\": {\n\t\t\t  \"palette\": \"dog_classic\",\n\t\t\t  \"line_type\": \"solid\",\n\t\t\t  \"line_width\": \"normal\"\n\t\t\t}\n\t\t  }\n\t\t],\n\t\t\"yaxis\": {\n\t\t  \"label\": \"\",\n\t\t  \"scale\": \"linear\",\n\t\t  \"min\": \"auto\",\n\t\t  \"max\": \"auto\",\n\t\t  \"include_zero\": true\n\t\t},\n\t\t\"title\": \"Anomalous CPU Activity\",\n\t\t\"time\": {},\n\t\t\"show_legend\": false\n\t  }\n\t}\n  ],\n  \"template_variables\": [\n\t{\n\t  \"name\": \"host\",\n\t  \"default\": \"gearbox09\",\n\t  \"prefix\": \"host\"\n\t}\n  ],\n  \"layout_type\": \"ordered\",\n  \"is_read_only\": true,\n  \"notify_list\": [\n\t\"jitkelme@gmail.com\"\n  ],\n  \"template_variable_presets\": [\n\t{\n\t  \"name\": \"Saved views for Gearbox09\",\n\t  \"template_variables\": [\n\t\t{\n\t\t  \"name\": \"host\",\n\t\t  \"value\": \"gearbox09\"\n\t\t}\n\t  ]\n\t}\n  ]\n}"
headers = {
    'Content-Type': "application/json",
    'DD-API-KEY': "<redacted>",
    'DD-APPLICATION-KEY': "<redacted>",
    'cache-control': "no-cache",
    'Postman-Token': "812c243d-8c26-466a-8ded-231e1ca3f958"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
