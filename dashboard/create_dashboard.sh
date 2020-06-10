#!/usr/bin/env bash

API_KEY=$1
APP_KEY=$2

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <DATADOG API KEY> <DATADOG APP KEY>"
  exit -1
fi

# create a datadog dashboard via its API
curl -X POST 'https://api.datadoghq.eu/api/v1/dashboard' \
	-H "DD-API-KEY: ${API_KEY}" \
  -H "DD-APPLICATION-KEY: ${APP_KEY}" \
	-H 'Content-Type: application/json' \
	-d @dashboard.json
