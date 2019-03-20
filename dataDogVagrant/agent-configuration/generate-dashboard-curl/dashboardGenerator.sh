
# !/bin/bash

api_key=ad00c177c779cc3d503ee10c55c302dd
app_key=dfd765459564830537d9cb5f0cce7ccd7b402cff

curl  -X POST -H "Content-type: application/json" \
-d @./widgets.json \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
