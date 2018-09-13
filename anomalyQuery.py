api_key=ba43f5ff300b9342eb4d993e32500157
app_key=631a76043f9c6825b5913e5d10b97e5c697409ac

curl -X POST -H "Content-type: application/json" \
-d '{
      "type": "metric alert",
      "query": "avg(last_1h):sum:postgresql.rows_returned{*} > 2"
}' \
    "https://api.datadoghq.com/api/v1/monitor/validate?api_key=${api_key}&application_key=${app_key}"
