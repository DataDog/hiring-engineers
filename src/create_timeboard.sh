#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=bdd8b3d81c8650acb71d9d34d1d93c98
app_key=a0fee8366974233dc7646c9c2f3d395cca92762c

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "Stigs random number",
          "definition": {
              "events": [
		{
		"q": "Interesting",
		"tags_execution": "and"
    		}
	      ],
              "requests": [
                {
		"q": "avg:my_metric{host:Stigs-MacBook-Pro.local}",
      		"type": "area",
      		"conditional_formats": [],
      		"aggregator": "avg"
		}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "Stigs random sum",
          "definition": {
              "events": [],
              "requests": [
                {
		"q": "avg:my_metric{host:Stigs-MacBook-Pro.local}.rollup(sum, 3600)",
      		"type": "bars",
      		"conditional_formats": [],
      		"aggregator": "avg"
                }
              ]
          },
          "viz": "timeseries"
      }

      ],
      "title" : "Stigs Timeboard",
      "description" : "This and that from Stigs Mac",
      "template_variables": [{
          "name": "Stigs-MacBook-Pro.local",
          "prefix": "host"
      }],
      "read_only": "True"
    }' "https://app.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
