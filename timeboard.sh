curl -X POST "https://api.datadoghq.eu/api/v1/dashboard" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{"title":"Timeboard",
"description":"",
"widgets":[
    {"definition":{
        "title":"my_metric",
        "title_size":"16",
        "title_align":"left",
        "show_legend":true,
        "legend_layout":"auto",
        "legend_columns":["avg","min","max","value","sum"],
        "time":{},
        "type":"timeseries",
        "requests":[{"formulas":[{"formula":"query1"}],
        "queries":[{"query":"avg:my_metric{*} by {host}","data_source":"metrics","name":"query1"}],
        "response_format":"timeseries",
        "style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}],
        "yaxis":{"include_zero":true,"scale":"linear","label":"","min":"auto","max":"auto"},
        "markers":[]
        }
    },
    {"definition":
        {
        "title":"mysql_anomalies",
        "title_size":"16",
        "title_align":"left",
        "show_legend":true,
        "legend_layout":"auto",
        "legend_columns":["avg","min","max","value","sum"],
        "time":{},
        "type":"timeseries",
        "requests":[
            {
                "formulas":[{"formula":"anomalies(query1, 'basic', 2)"}],
                "queries":[{"data_source":"metrics","name":"query1","query":"avg:mysql.net.connections{*}"}],
                "response_format":"timeseries",
                "on_right_yaxis":false,
                "style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}
        ],
        "yaxis":{"scale":"linear","include_zero":true,"label":"","min":"auto","max":"auto"},
        "markers":[]
        }
    },
    {"definition":{"title":"my_metric_rollup","title_size":"16",
        "title_align":"left",
        "show_legend":true,
        "legend_layout":"auto",
        "legend_columns":["avg","min","max","value","sum"],
        "time":{},
        "type":"timeseries",
        "requests":[{"formulas":[{"formula":"query1"}],
        "queries":[{"data_source":"metrics","name":"query1","query":"avg:my_metric{*}.rollup(sum, 3600)"}],
        "response_format":"timeseries",
        "style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}],
        "yaxis":{"scale":"linear","include_zero":true,"label":"","min":"auto","max":"auto"},
        "markers":[]
        }
    }
],
"template_variables":[],
"layout_type":"ordered",
"is_read_only":false,
"notify_list":[],
"reflow_type":"auto"
}
EOF