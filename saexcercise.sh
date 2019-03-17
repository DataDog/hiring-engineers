#!/bin/bash

api_key=8923495892e42d2b7919f8764641d254
app_key=f75db8c09aaa5bc351c9d1d983c98fda24d98d43

curl  -X POST -H "Content-type: application/json" \
-d @./json/sadashboard.json \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"

curl -X POST -H "Content-type: application/json" \
-d @./json/samonitor.json \
"https://api.datadoghq.com/api/v1/monitor?api_key=${api_key}&application_key=${app_key}"

curl -X POST -H "Content-type: application/json" \
-d @./json/sadowntime.json \
"https://api.datadoghq.com/api/v1/downtime?api_key=${api_key}&application_key=${app_key}"

curl -X POST -H "Content-type: application/json" \
-d @./json/sadowntimeweekend.json \
"https://api.datadoghq.com/api/v1/downtime?api_key=${api_key}&application_key=${app_key}"
