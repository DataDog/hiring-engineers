api_key="XXXXX"
app_key="XXXX"

curl  -X POST \
-H "Content-type: application/json" \
-H "DD-API-KEY: ${api_key}" \
-H "DD-APPLICATION-KEY: ${app_key}" \
-d '{
	"title": "My API-Defined Dashboard 0416201906", 
	"widgets": [{
			"definition": {
				"type": "timeseries",
				"requests": [{
					"q": "avg:my_metric{host:ramy.abdelazim}"
				}],
				"title": "My Metric per Host"
			}
		},
		{
			"definition": {
				"type": "timeseries",
				"requests": [{
					"q": "anomalies(mysql.innodb.rows_read{*}, \"basic\", 2)"
				}],
				"title": "MySQL anomalies"
			}
		},
		{
			"definition": {
				"type": "timeseries",
				"requests": [{
					"q": "sum:my_metric{host:ramy.abdelazim}.rollup(sum, 3600)"
				}],
				"title": "My Metric Rollup"
			}
		}
	],
	"layout_type": "ordered",
	"description": "Dashboard with a few widgets",
	"notify_list": ["ramyfromakamai@gmail.com"]
}' \
"https://api.datadoghq.com/api/v1/dashboard"


