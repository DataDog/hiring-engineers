# This script was used as a convenience script for clearing out dashboards I created using dashboard.py when I was testing out various
# widgets and parameters.  This script allowed me to clean up my environment for when I created the final dashboard with the script found
# in dashboard.py

from datadog import initialize, api

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

dashboards = api.Dashboard.get_all()

count = 0

for d in dashboards["dashboards"]:
    print("Removing dashboard" + d["id"])
    api.Dashboard.delete(d["id"])
    count+=1

print("Removed " + str(count) + " dashboards succesfully!")