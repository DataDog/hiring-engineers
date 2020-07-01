api_key=75cc324da0bc265b8883ce646853b814
app_key=90010fe90c75c6ba58575f40fe0b5831b2db00fd

curl  -X POST -H "Content-type: application/json" \
-d '{
   "title":"Example Timeboard",
   "description":"Timeboard created with API",
   "widgets":[
      {
         "id":947107672124808,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"avg:my_metric{host:datadog1}",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"My Customer Metric",
            "time":{

            },
            "show_legend":false,
            "legend_size":"0"
         }
      },
      {
         "id":2150531279346304,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"avg:mysql.performance.com_select{host:datadog1}",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"MySQL Performance Select",
            "time":{

            },
            "show_legend":false,
            "legend_size":"0"
         }
      },
      {
         "id":1013625373256536,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"sum:my_metric{host:datadog1}.rollup(sum, 60)",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"My Metric Rollup",
            "time":{

            },
            "show_legend":false
         }
      }
   ],
   "template_variables":[

   ],
   "layout_type":"ordered",
   "is_read_only":false,
   "notify_list":[

   ],
   "id":"x4r-ccw-z5s"
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"