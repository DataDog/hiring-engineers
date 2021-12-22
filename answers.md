Your answers to the questions go here.

Getting Metrics:
1. Image: ![image](https://user-images.githubusercontent.com/96433227/146793385-14a81adb-dd83-4e8a-b7a7-a50969077dd5.png)

   yaml file: ![image](https://user-images.githubusercontent.com/96433227/146793490-fb43bdba-c3b0-4453-ac3f-c6aea3445b34.png)
   
   Datadog Agent Manager: ![image](https://user-images.githubusercontent.com/96433227/146793571-7df54eac-2694-4aa0-9975-d67819c354d9.png)
   
2. MongoDB Installed: ![image](https://user-images.githubusercontent.com/96433227/146794365-5a45d99d-86c3-40c0-9239-4faf04831771.png)

3. Random Number Generator:

code: ![image](https://user-images.githubusercontent.com/96433227/146829641-2408964f-0f0c-4c7c-9372-729c2bf50086.png)

graph: ![image](https://user-images.githubusercontent.com/96433227/146827897-3d3ef2a3-5133-4b94-ac8e-c0a0f038ce40.png)

4. Collection Interval:

code: ![image](https://user-images.githubusercontent.com/96433227/146829674-6fe9fc70-8cd2-44da-83bb-b67cb363f2aa.png)

graph: ![image](https://user-images.githubusercontent.com/96433227/146829130-c4684b45-f4fb-455c-89db-1f874195589d.png)

Visualizing Data:
1. Snapshot to myself: ![image](https://user-images.githubusercontent.com/96433227/147123303-44c50a09-2b0d-43d5-936f-76693ca0cef3.png)

Dashboard: ![image](https://user-images.githubusercontent.com/96433227/147124712-a6d9d995-9444-4879-bea4-56a1e87c597f.png)

Note: I couldn't get the data from my MongoDB to send to Datadog. I tried to configure the mongo.d/conf.yaml file to create a custom query but couldn't get that to send either so I moved on to the next part.

If there was an anomaly graph, it would use the stats it collected to show the data that is 2 deviations outside the standard norm. 

Code used: 

curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--data-raw '{
"title": "My_Metric over Host",
  "description": "The custom check My_Metric displayed over time.",
  "widgets": [
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "my_metric{host:mrsclause}",
                        "display_type":"line",
                        "style":{
                            "palette": "green",
                            "line_type":"solid",
                            "line_width":"normal"
                        }
                  }
                ],
                "title": "My Hourly Metric",
                "show_legend": false,
                "legend_size": "0"
          }
        },
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "sum:my_metric{host:mrsclause}.rollup(sum, 3600)",
                        "display_type": "line",
                        "style": {
                          "palette": "red",
                          "line_type": "dashed",
                          "line_width": "thick"
                        }
                  }
                ],
                "yaxis": {
                  "label": "",
                  "scale": "linear",
                  "min": "auto",
                  "max": "auto",
                  "include_zero": true
                },
                "title": "Sum of Points Hourly",
                "time": {},
                "show_legend": false,
                "legend_size": "0"
          }
        },
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "anomalies(avg:mongodb.atlas.system.disk.space.free{host:mrsclause}, \"basic\", 2)",
                        "display_type": "line",
                        "style": {
                          "palette": "dog_classic",
                          "line_type": "solid",
                          "line_width": "normal"
                        }
                  }
                ],
                "yaxis": {
                  "label": "",
                  "scale": "linear",
                  "min": "auto",
                  "max": "auto",
                  "include_zero": true
                },
                "title": "Database Integration Metric",
                "time": {},
                "show_legend": false
          }
        }
  ],
  "template_variables": [
        {
          "name": "host",
          "default": "mrsclause",
          "prefix": "host"
        }
  ],
  "layout_type": "ordered",
  "is_read_only": true,
  "template_variable_presets": [
        {
          "name": "Saved views for Mrsclause",
          "template_variables": [
                {
                  "name": "host",
                  "value": "mrsclause"
                }
          ]
        }
  ]
}'
