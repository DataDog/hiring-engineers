#!/bin/bash

api_key="2b26fb6c0ab7bd38a6a5fc3de677dd22"
app_key="256bc13bf7b6adf82609c8b007f3695e961dafe8"

curl  -X POST -H "Content-type: application/json" \
-T timeboard.json \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

curl -X POST -H "Content-type: application/json" \
-T monitor.json \
"https://api.datadoghq.com/api/v1/monitor?api_key=${api_key}&application_key=${app_key}"
