from datadog import initialize, api

options = {
    'api_key': '******',
    'app_key': '******'
}

initialize(**options)

title = 'my_metric dashboard!'
widgets = [
    {
      "definition": {
        "title": "my_metric scoped over host CPU",
        "title_size": "16",
        "title_align": "left",
        "show_legend": True,
        "legend_layout": "auto",
        "legend_columns": [
          "avg",
          "min",
          "max",
          "value",
          "sum"
        ],
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:system.cpu.user{*}",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "line"
          },
          {
            "q": "avg:my_metric{*}",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "line"
          }
        ],
        "yaxis": {
          "scale": "linear",
          "label": "",
          "include_zero": True,
          "min": "auto",
          "max": "auto"
        },
        "markers": []
      }
    },
    {
      "definition": {
        "title": "MySQL Connections (with Anomalies)",
        "title_size": "16",
        "title_align": "left",
        "show_legend": True,
        "legend_layout": "auto",
        "legend_columns": [
          "avg",
          "min",
          "max",
          "value",
          "sum"
        ],
        "type": "timeseries",
        "requests": [
          {
            "q": "anomalies(avg:mysql.net.connections{*}, 'basic', 3)",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "line"
          }
        ],
        "yaxis": {
          "scale": "linear",
          "label": "",
          "include_zero": True,
          "min": "auto",
          "max": "auto"
        },
        "markers": []
      }
    },
    {
      "definition": {
        "title": "my_metric sum for the hour",
        "title_size": "16",
        "title_align": "left",
        "type": "query_value",
        "requests": [
          {
            "q": "avg:my_metric{*}.rollup(sum, 3600)",
            "aggregator": "avg"
          }
        ],
        "autoscale": True,
        "precision": 2
      }
    },
    {
      "definition": {
        "title": "My Host Map",
        "title_size": "16",
        "title_align": "left",
        "type": "hostmap",
        "requests": {
          "fill": {
            "q": "avg:system.cpu.user{*} by {host}"
          }
        },
        "node_type": "host",
        "no_metric_hosts": True,
        "no_group_hosts": True,
        "style": {
          "palette": "Viridis",
          "palette_flip": False
        }
      }
    },
    {
      "definition": {
        "title": "Top Host Processes (Total CPU%)",
        "title_size": "16",
        "title_align": "left",
        "time": {},
        "type": "toplist",
        "requests": [
          {
            "process_query": {
              "search_by": "",
              "filter_by": [],
              "limit": 10,
              "metric": "process.stat.cpu.total_pct"
            }
          }
        ]
      }
    }
  ]
layout_type = 'ordered'
description = 'A dashboard created with the API'
is_read_only = True

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only)
