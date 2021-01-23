# This script was used as a convenience script for clearing out dashboards I created using dashboard.py when I was testing out various
# widgets and parameters.  This script allowed me to clean up my environment for when I created the final dashboard with the script found
# in dashboard.py

from datadog import initialize, api

options = {
    'api_key': 'ab871a5b035a46c7b9bde8c3fa396bfd',
    'app_key': 'a523b3786ada231d5ac24f0a01ce1622fe1619a3'
}

initialize(**options)

dashboards = api.Dashboard.get_all()

count = 0

for d in dashboards["dashboards"]:
    print("Removing dashboard" + d["id"])
    api.Dashboard.delete(d["id"])
    count+=1

print("Removed " + str(count) + " dashboards succesfully!")