#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=103ab67be31f058848dbd337504e8aed
app_key=685c531fa53f779185ec48d7c1d364b86b8fd8f6
host=YourHostName

# Find a host to add a tag to
host_name=$(curl -G "https://app.datadoghq.com/api/v1/search" \
    -d "api_key=${api_key}" \
    -d "application_key=${app_key}" \
    -d "q=hosts:$host" | cut -d'"' -f6)

curl  -X POST -H "Content-type: application/json" \
-d "{
      \"tags\" : [\"environment:production\", \"role:webserver\"]
    }" \
"https://app.datadoghq.com/api/v1/tags/hosts/${host_name}?api_key=${api_key}&application_key=${app_key}"