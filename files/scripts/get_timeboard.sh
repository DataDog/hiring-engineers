#!/bin/bash
# delete timeboard
api_key=<api_key>
app_key=<app_key>
dash_id=$1


curl "https://app.datadoghq.com/api/v1/dash/${dash_id}?api_key=${api_key}&application_key=${app_key}"