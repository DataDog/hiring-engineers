#!/bin/bash

if [ -z "$2" ] 
then
  curl -X POST -H "Content-type: application/json" -d @$1 "https://app.datadoghq.com/api/v1/dash?api_key=?api_key=${DD_API_KEY}&application_key=${DD_APP_KEY}"
else
  curl -X PUT -H "Content-type: application/json" -d @$1 "https://app.datadoghq.com/api/v1/dash/${2}?api_key=${DD_API_KEY}&application_key=${DD_APP_KEY}"
fi
