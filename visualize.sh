#!/bin/sh
# This script is part 1 of the requirements for the Datadog Technical Exercise

api_key=9d6d81e95d0d9417bb7a6d321a517a5a
app_key=f05603588fcbc601e37765a02f03564559863e01

curl -X POST -H "Content-type: application/json" \
-d '{
"title":"Technical Exercise Timeboard v3",
"description":"Created today",
        "graphs":[
{
                "definition":{
                    "viz":"timeseries",
                    "requests":[
                        {
                            "q":"avg:system.cpu.user{*}",
                            "style":{
                                "palette":"dog_classic",
                                "width":"normal",
                                "type":"solid"
                            },
                            "type":"line"
                        }
                    ]
                },
                "title":"System Load Over Time"
            },
            {
                "definition":{
                    "viz":"timeseries",
                    "requests":[
                        {
                            "q":"avg:my_metric{role:database} by {host}.rollup(sum, 60)",
                            "style":{
                                "palette":"dog_classic",
                                "width":"normal",
                                "type":"solid"
                            },
                            "type":"area"
                        }
                    ]
                },
                "title":"My_Metric with Rollup"
            }
        ],
        "template_variables":[
        ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

# Notes: JSON for the third portion does not work when submitted against the API.  The code was taken directly from both the UI and a query to get JSON data.
# The following snippet causes an error when added to the graphs section:
# Error message:
#{"errors": ["Error parsing query: unable to parse anomalies(avg:mysql.net.connections{role:database}, basic, 2): Rule 'scope_expr' didn't match at ', 2)' (line 1, column 58)."]}
#,
#         {
#            "definition":{
#               "viz":"timeseries",
#               "requests":[
#                  {
#                     "q":"anomalies(avg:mysql.net.connections{role:database}, 'basic', 2)",
#                     "style":{
#                        "palette":"dog_classic",
#                        "width":"normal",
#                        "type":"solid"
#                     },
#                     "type":"line"
#                  }
#               ]
#            },
#            "title":"Aborted Database Connections"
#         }