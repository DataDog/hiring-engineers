#!/bin/bash
curl -X GET "https://app.datadoghq.com/api/v1/dash/${2}?api_key=${DD_API_KEY}&application_key=${DD_APP_KEY}" > ${1}
