curl -X POST "https://api.datadoghq.eu/api/v1/dashboard" -H "Content-Type: application/json" -H "DD-API-KEY: 41ebe5195ac8082687a23859447a1955" -H "DD-APPLICATION-KEY: ba7b95a0342a805120814bab2d06d7cc5c42cba5" -d @- << EOF
{
  "layout_type": "ordered",
  "template_variables": [
    {
      "name": "ismas.random.number.generator"
    }
  ],
  "title": "It's never too much lasagna",
  "widgets": [
    {
      "definition": {
        "requests": [
          {
            "formulas": [
              {
                "formula": "query1"
              }
            ],
            "style": {
              "line_width": "normal",
              "palette": "dog_classic",
              "line_type": "solid"
            },
            "display_type": "line",
            "response_format": "timeseries",
            "queries": [
              {
                "query": "avg:ismas.random.number.generator{*}",
                "data_source": "metrics",
                "name": "query1"
              }
            ]
          }
        ],
        "type": "timeseries",
        "title_size": "16",
        "legend_columns": [
          "avg",
          "min",
          "max",
          "value",
          "sum"
        ],
        "yaxis": {
          "include_zero": true,
          "max": "auto",
          "scale": "linear",
          "min": "auto",
          "label": ""
        },
        "title_align": "left",
        "markers": [],
        "legend_layout": "auto",
        "show_legend": true,
        "time": {},
        "title": "my custom host scooped metric"
      },
      "layout": {
        "height": 5,
        "width": 6,
        "x": 0,
        "y": 5
      }
    },
    {
      "definition": {
        "requests": [
          {
            "formulas": [
              {
                "formula": "anomalies(query2, 'basic', 2)"
              }
            ],
            "style": {
              "line_width": "normal",
              "palette": "dog_classic",
              "line_type": "solid"
            },
            "display_type": "line",
            "response_format": "timeseries",
            "queries": [
              {
                "query": "avg:mongodb.opcounters.commandps{*}",
                "data_source": "metrics",
                "name": "query2"
              }
            ]
          }
        ],
        "type": "timeseries",
        "title_size": "16",
        "legend_columns": [
          "avg",
          "min",
          "max",
          "value",
          "sum"
        ],
        "yaxis": {
          "include_zero": true,
          "max": "auto",
          "scale": "linear",
          "min": "auto",
          "label": ""
        },
        "title_align": "left",
        "markers": [],
        "legend_layout": "auto",
        "show_legend": true,
        "time": {},
        "title": "mongodb.opcounters.commandps average"
      },
      "layout": {
        "height": 5,
        "width": 6,
        "x": 6,
        "y": 5
      }
    },
    {
      "definition": {
        "requests": [
          {
            "formulas": [
              {
                "formula": "query3"
              }
            ],
            "response_format": "scalar",
            "queries": [
              {
                "query": "avg:ismas.random.number.generator{*}.rollup(sum, 3600)",
                "data_source": "metrics",
                "name": "query3",
                "aggregator": "avg"
              }
            ]
          }
        ],
        "type": "query_value",
        "title_size": "16",
        "title_align": "left",
        "time": {},
        "title": "Result from adding up 1 hour of random numbers, but in a really big box"
      },
      "layout": {
        "height": 3,
        "width": 12,
        "x": 0,
        "y": 0
      }
    }
  ]
}
EOF
