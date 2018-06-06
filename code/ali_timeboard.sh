curl  -X POST -H "Content-type: application/json" \
-d '{
  "graphs" : [{
     "title": "My Metric Over Host",
     "definition": {
         "requests": [
			  {"q": "avg:my_metric{host:alishaw}"}
		  ]
     },
     "viz": "timeseries"
 },
 {
     "title": "MongoDB with anomalies",
     "definition": {
         "requests": [
             {"q": "anomalies(avg:mongodb.connections.available{host:alishaw},'basic', 2)"}
	     ]
	 },
     "viz": "timeseries"
 },
 {
     "title": "My Metric Rollup Sum",
     "definition": {
         "requests": [
             {"q": "avg:my_metric{host:alishaw}.rollup(sum, 3600)"}
		 ]
	 },
     "viz": "timeseries"
 }      
 ],
 "title" : "Alis Challenge Timeboard v2",
 "description" : "A timeboard to visualise my challenge",
 "template_variables": [{
     "name": "host1",
     "prefix": "host",
     "default": "host:my-host"
 }],
 "read_only": "True"
 }' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"