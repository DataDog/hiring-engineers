curl -X POST "https://api.datadoghq.eu/api/v1/dashboard" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_CLIENT_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_CLIENT_APP_KEY}" \
-d @- << EOF
{
   "title":"Visualizing Data",
   "description":"Visualizing Data",
   "layout_type":"ordered",
   "widgets":[
      {
         "definition":{
            "title":"My Metric",
            "type":"timeseries",
            "requests":[
               {
                  "q":"my_metric{host:JohnLinuxWsl}",
                  "display_type":"line",
                  "style":{
                     "line_type":"solid",
                     "line_width":"normal",
                     "palette":"Cool"
                  }
               }
            ],
            "yaxis":{
               "scale":"linear",
               "include_zero":true,
               "min":"auto",
               "max":"auto"
            }
         }
      },
      {
         "definition":{
            "title":"anomalies",
            "show_legend":false,
            "type":"timeseries",
            "requests":[
               {
                  "q":"anomalies(avg:mysql.performance.cpu_time{host:JohnLinuxWsl}, 'agile', 2)",
                  "display_type":"line",
                  "style":{
                     "line_type":"solid",
                     "line_width":"normal",
                     "palette":"Cool"
                  }
               }
            ],
            "yaxis":{
               "scale":"linear",
               "include_zero":true,
               "min":"auto",
               "max":"auto"
            }
         }
      },
      {
         "definition":{
            "title":"Hourly Rollup",
            "show_legend":false,
            "type":"timeseries",
            "requests":[
               {
                  "q":"sum:my_metric{host:JohnLinuxWsl}.rollup(sum, 3600)",
                  "display_type":"line",
                  "style":{
                     "line_type":"solid",
                     "line_width":"normal",
                     "palette":"Cool"
                  }
               }
            ],
            "yaxis":{
               "scale":"linear",
               "include_zero":true,
               "min":"auto",
               "max":"auto"
          }
         }
      },
            {
         "definition":{
            "title":"30 Sec Rollup",
            "show_legend":false,
            "type":"timeseries",
            "requests":[
               {
                  "q":"sum:my_metric{host:JohnLinuxWsl}.rollup(sum, 30)",
                  "display_type":"line",
                  "style":{
                     "line_type":"solid",
                     "line_width":"normal",
                     "palette":"Cool"
                  }
               }
            ],
            "yaxis":{
               "scale":"linear",
               "include_zero":true,
               "min":"auto",
               "max":"auto"
          }
         }
      }
   ]
}
EOF
```