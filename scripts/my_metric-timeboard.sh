#!/bin/bash

api_key="<MY_API_KEY>"
app_key="<MY_APP_KEY>"

curl  -X POST -H "Content-type: application/json" \
-T timeboard.json \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

curl -X POST -H "Content-type: application/json" \
-T monitor.json \
"https://api.datadoghq.com/api/v1/monitor?api_key=${api_key}&application_key=${app_key}"
