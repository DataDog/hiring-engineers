## Visualizing Data
curl -X "POST" "https://app.datadoghq.eu/api/v1/dash?api_key=d3086d9ee6433b3af5e47a2eb5485abf&application_key=ed4a5264bbf6f6e3a30a16de72fd76e3b9133797" \
     -H 'Content-Type: application/json' \
     -H 'Cookie: DD-PSHARD=0' \
     -d $'{
  "title": "Steffens Timeboard",
  "graphs": [
    {
      "title": "Steffens heating consumption",
      "definition": {
        "requests": [
          {
            "aggregator": "avg",
            "q": "avg:HZ_Usage_kWh{host:raspberrypi}",
            "type": "area",
            "conditional_formats": []
          }
        ],
        "events": [
          {
            "q": "Interesting",
            "tags_execution": "and"
          }
        ]
      },
      "viz": "timeseries"
    },
    {
      "title": "Steffens consumption sum",
      "definition": {
        "requests": [
          {
            "aggregator": "avg",
            "q": "avg:HZ_Usage_kWh{host:raspberrypi}.rollup(sum, 3600)",
            "type": "bars",
            "conditional_formats": []
          }
        ],
        "events": []
      },
      "viz": "timeseries"
    }
  ],
  "description": "All from my Pi",
  "template_variables": [
    {
      "name": "raspberrypi",
      "prefix": "host"
    }
  ],
  "read_only": "True"
}'
