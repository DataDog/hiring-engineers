curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--header 'DD-API-KEY: <REDACTED>' \
--header 'DD-APPLICATION-KEY: <REDACTED>' \
 \
--data-raw '{
   "title":"lkamakura Anomaly Timeboard",
   "description":"## lkamakura Anomaly Timeboard\n\nCustom metric, MySql with anomaly function, Custom metric with rollup function applied.",
   "widgets":[
      {
         "id":6211391627065367,
         "definition":{
            "title":"my_check Timeseries",
            "title_size":"16",
            "title_align":"left",
            "show_legend":false,
            "type":"timeseries",
            "requests":[
               {
                  "q":"avg:my_check{*}",
                  "display_type":"line"
               }
            ]
         },
         "layout":{
            "x":0,
            "y":0,
            "width":4,
            "height":2
         }
      },
      {
         "id":2998384763068902,
         "definition":{
            "title":"MySQL Insert Anomaly Monitor",
            "title_size":"16",
            "title_align":"left",
            "show_legend":true,
            "legend_layout":"auto",
            "legend_columns":[
               "avg",
               "min",
               "max",
               "value",
               "sum"
            ],
            "type":"timeseries",
            "requests":[
               {
                  "formulas":[
                     {
                        "alias":"rows inserted per second",
                        "formula":"anomalies(query1, '\''basic'\'', 2)"
                     }
                  ],
                  "response_format":"timeseries",
                  "queries":[
                     {
                        "query":"avg:mysql.innodb.rows_inserted{*}",
                        "data_source":"metrics",
                        "name":"query1"
                     }
                  ],
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  },
                  "display_type":"line"
               }
            ],
            "yaxis":{
               "include_zero":true,
               "scale":"linear",
               "label":"",
               "min":"auto",
               "max":"auto"
            },
            "markers":[
               
            ]
         },
         "layout":{
            "x":4,
            "y":0,
            "width":4,
            "height":2
         }
      },
      {
         "id":2397295511845380,
         "definition":{
            "title":"my_check Aggregated Over the Last Hour",
            "title_size":"16",
            "title_align":"left",
            "show_legend":true,
            "legend_layout":"auto",
            "legend_columns":[
               "avg",
               "min",
               "max",
               "value",
               "sum"
            ],
            "type":"timeseries",
            "requests":[
               {
                  "formulas":[
                     {
                        "formula":"query1"
                     }
                  ],
                  "response_format":"timeseries",
                  "queries":[
                     {
                        "query":"avg:my_check{*}.rollup(sum, 3600)",
                        "data_source":"metrics",
                        "name":"query1"
                     }
                  ],
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  },
                  "display_type":"line"
               }
            ],
            "yaxis":{
               "include_zero":true,
               "scale":"linear",
               "label":"",
               "min":"auto",
               "max":"auto"
            },
            "markers":[
               
            ]
         },
         "layout":{
            "x":8,
            "y":0,
            "width":4,
            "height":2
         }
      }
   ],
   "template_variables":[
      {
         "name":"host1",
         "default":"*",
         "available_values":[
            
         ]
      }
   ],
   "layout_type":"ordered",
   "is_read_only":false,
   "notify_list":[
      
   ],
   "reflow_type":"fixed",
   "id":"3kd-3vm-xsk"
}'
