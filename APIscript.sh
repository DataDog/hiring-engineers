# Curl command
curl -X POST https://api.datadoghq.com/api/v1/dashboard \
-H "Content-Type: application/json" \
-H "DD-API-KEY: " \
-H "DD-APPLICATION-KEY: " \
-d @- << EOF
{
	"title": "RG Testing 5",
	"description": "<DASHBOARD_DESCRIPTION>",
	"widgets": [{
		"id": 5207595062780050,
		"definition": {
			"type": "hostmap",
			"requests": {
				"fill": {
					"q": "avg:my_metric{host:rg-dd-ubuntu} by {host}"
				},
				"size": {
					"q": "avg:my_metric{host:rg-dd-ubuntu} by {host}"
				}
			},
			"title": "My Metric Scoped to Host RG-DD-Ubuntu",
			"node_type": "host",
			"no_metric_hosts": false,
			"no_group_hosts": true,
			"scope": ["host:rg-dd-ubuntu"],
			"style": {
				"palette": "green_to_orange",
				"palette_flip": false,
				"fill_min": "0",
				"fill_max": "825"
			}
		}
	}, {
		"id": 7464484663075336,
		"definition": {
			"type": "timeseries",
			"requests": [{
				"q": "avg:my_metric{host:rg-dd-ubuntu}",
				"display_type": "line",
				"style": {
					"palette": "dog_classic",
					"line_type": "solid",
					"line_width": "normal"
				},
				"on_right_yaxis": false
			}],
			"yaxis": {
				"label": "",
				"scale": "linear",
				"min": "auto",
				"max": "auto",
				"include_zero": true
			},
			"title": "Avg of My Metric Over Host RG-DD-Ubuntu",
			"show_legend": false,
			"legend_size": "0"
		}
	}, {
		"id": 2561966657179646,
		"definition": {
			"type": "timeseries",
			"requests": [{
				"q": "anomalies(avg:mysql.net.connections{host:rg-dd-ubuntu}, 'basic', 2)",
				"display_type": "line",
				"style": {
					"palette": "dog_classic",
					"line_type": "solid",
					"line_width": "normal"
				}
			}],
			"yaxis": {
				"label": "",
				"scale": "linear",
				"min": "auto",
				"max": "auto",
				"include_zero": true
			},
			"title": "Avg of mysql.net.connections over Host RG-DD-Ubuntu",
			"show_legend": false,
			"legend_size": "0"
		}
	}, {
		"id": 2760035264495996,
		"definition": {
			"type": "timeseries",
			"requests": [{
				"q": "avg:my_metric{*}.rollup(sum, 3600)",
				"display_type": "bars",
				"style": {
					"palette": "dog_classic",
					"line_type": "solid",
					"line_width": "normal"
				},
				"on_right_yaxis": false
			}],
			"yaxis": {
				"label": "",
				"scale": "linear",
				"min": "auto",
				"max": "auto",
				"include_zero": true
			},
			"title": "My metric roll up sum past hour",
			"show_legend": false,
			"legend_size": "0"
		}
	}, {
		"id": 793196778974279,
		"definition": {
			"type": "timeseries",
			"requests": [{
				"q": "avg:system.mem.free{*}"
			}],
			"title": "Average Memory Free",
			"show_legend": false,
			"legend_size": "0"
		}
	}],
	"template_variables": [{
		"name": "host",
		"default": "<HOSTNAME_1>",
		"prefix": "host"
	}],
	"layout_type": "ordered",
	"is_read_only": true,
	"notify_list": [],
	"template_variable_presets": [{
		"name": "Saved views for hostname 2",
		"template_variables": [{
			"name": "host",
			"value": "<HOSTNAME_2>"
		}]
	}],
	"id": "gwm-8cq-usy"
}
EOF
