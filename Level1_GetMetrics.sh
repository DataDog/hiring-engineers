#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=103ab67be31f058848dbd337504e8aed
app_key=685c531fa53f779185ec48d7c1d364b86b8fd8f6

from_time=$(date -v -1d +%s)

curl -G \
    "https://app.datadoghq.com/api/v1/metrics" \
    -d "api_key=${api_key}" \
    -d "application_key=${app_key}" \
    -d "from=${from_time}"