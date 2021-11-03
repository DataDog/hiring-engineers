# from datadog import initialize, api
# Download JSON from datadog dashboard:

# {"title":"Delaney's Dashboard",
#     "description":"",
#     "widgets":[],
#     "template_variables":[],
#     "layout_type":"ordered",
#     "is_read_only":false,
#     "notify_list":[],
#     "reflow_type":"auto",
#     "id":"tgx-try-vyn"}

#Data2Dog Visualiziation:
# options = {
#     'api_key': '1589e4066ca4bc3cab3a8676b1e55a89'
# ,
#     'app_key': '55cd01bdafc7e69dadf3f275b25113b41e834899'
# }
#   "title": "Delaney's Dashboard",
#   "description": "A custom timeboard.",
#   "widgets": [
#         {
#           "definition": {
#                 "type": "timeseries",
#                 "requests": [
#                   {
#                         "q": "my_metric{*}"
#                   }
#                 ],
#                 "title": "My Custom Metric",
#                 "show_legend": false,
#                 "legend_size": "0"
#           }
#         },
#         {
#           "definition": {
#                 "type": "timeseries",
#                 "requests": [
#                   {
#                         "q": "avg:my_metric{*}.rollup(sum, 3600)",
#                         "metadata": [
#                           {
#                                 "expression": "sum:my_metric{host:gearbox09.dev.controlplane.info}.rollup(sum, 3600)",
#                                 "alias_name": "my_hour"
#                           }
#                         ],
#                         "display_type": "line",
#                         "style": {
#                           "palette": "dog_classic",
#                           "line_type": "solid",
#                           "line_width": "normal"
#                         }
#                   }
#                 ],
#                 "yaxis": {
#                   "label": "",
#                   "scale": "linear",
#                   "min": "auto",
#                   "max": "auto",
#                   "include_zero": true
#                 },
#                 "title": "My Hourly Rollup",
#                 "time": {},
#                 "show_legend": false,
#                 "legend_size": "0"
#           }
#         },
#         {

#             #MongoDB 
#           "definition": {
#                 "type": "timeseries",
#                 "requests": [
#                   {
#                         "q": "anomalies(avg:mysql.performance.cpu_time{host:gearbox09.dev.controlplane.info}, '\''basic'\'', 2)",
#                         "display_type": "line",
#                         "style": {
#                           "palette": "dog_classic",
#                           "line_type": "solid",
#                           "line_width": "normal"
#                         }
#                   }
#                 ],
#                 "yaxis": {
#                   "label": "",
#                   "scale": "linear",
#                   "min": "auto",
#                   "max": "auto",
#                   "include_zero": true
#                 },
#                 "title": "Anomalous CPU Activity",
#                 "time": {},
#                 "show_legend": false
#           }
#         }
#   ],
#   "template_variables": [
#         {
#           "name": "host",
#           "default": "gearbox09",
#           "prefix": "host"
#         }
#   ],
#   "layout_type": "ordered",
#   "is_read_only": true,
#   "notify_list": [
#         "jitkelme@gmail.com"
#   ],
#   "template_variable_presets": [
#         {
#           "name": "Saved views for Gearbox09",
#           "template_variables": [
#                 {
#                   "name": "host",
#                   "value": "gearbox09"
#                 }
#           ]
#         }
#   ]
# }'