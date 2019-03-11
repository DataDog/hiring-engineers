Your answers to the questions go here.

Collecting Metrics:

1.Host agent installation: 

Created a windows server 2019 WDog3 and installed agent using the https://app.datadoghq.com/account/settings#agent/windows instructions.
	
Added tags to the installation

	msiexec /qn /i datadog-agent-6-latest.amd64.msi APIKEY="c657bdea00effba8c512cb5056a473ac" 
	HOSTNAME="WDog3" 
	TAGS="Windows, Test,Azure,W2K19"

Learned that the Datadog Agent ver 6 has its own bundled Python Environment and its management interface on localhost port 5002
Uploaded Files: Tags_from_Agent_setting.png, Tags_from_Host_Map.png

2 MongoDB installation:

Installed MongoDB Enterprise and uploaded a test database with script. Enabled Authentication as it is disabled by default.
Was challenged by the DOC’s for the windows agent.
1.	It is clear that the Windows Agents mondo.d /conf.yaml is based on the Linux version so you have to make changes to it for getting the log agent to run correctly.

Changed from:


 	path: /var/log/mongodb/mongodb.log
 	service: mongo
 	source: mongodb

To

	path: C:\Program Files\MongoDB\Server\4.0\log\mongod.log
	service: mongodb
 	source: mongodb

Which is the default path to the Mongodb log on my install.
Suggestion:  Correct the all the help files for the Windows agent to the correct syntax.
Eventually got the metrics and the logs collection work
Important to note that agent needs to be restarted after every change as it needs to refresh the configuration
 
3 Create a custom Agent Check:

Found Docs for doing this here
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
Used the randint function from the random module as in trace example 
Found it here
https://docs.datadoghq.com/api/?lang=python#send-traces

Kept the version check of the Agent in the python file.

Important that the files are in the root of the conf.d and checks.d directories

Created file custom_check.yaml in conf.d:

And custom_check.py  in checks.d:


I then used the “Add a Check” on DataDog Agent Manager interface to add the custm_check.yaml to the checks

4 Bonus Question: 

User the Edit Enabled Checks function in the Datadog Agent Manager and change the  
- min_collection_interval: in the custom_check.yaml check.

See uploaded Edit custom_check.yaml.png

Visualizing data:

1. Working around Datadog Python API DataPy ver 0.26.0 challenges:

I installed Python and PIP then installed the Datadog API python (Datadogpy) module version 0.26.0 using PIP.
I started playing around with a python example: 
https://docs.datadoghq.com/api/?lang=python#create-a-dashboard
I then discovered that the module was broken or the documentation was incorrect
    AttributeError: module 'datadog.api' has no attribute 'dashboard'

I then checked

https://github.com/DataDog/datadogpy/commit/80aa291429b73bfb2ceb73be0874e6e1c4570d96
https://datadogpy.readthedocs.io/en/latest/ 

Which shows that the documentation was correct as the endpoint was in the source files

I could not back rev as previous version 0.25.0 did not have the Dashboard endpoint and looking at its documentation its clear its an addition in ver 0.26.0

So I :
Uninstalled the datadog module  using PIP
And instead I downloaded the source code from Git hub and installed it using the install.py script 
https://github.com/DataDog/datadogpy
sudo python setup.py install
NOTE:
(( Revisited the issue 7th of March and can se vaerion 0.27.0 is available with the addition in the change log

			# 0.27.0 / 2019-03-06
			

			**New Dashboards API: https://docs.datadoghq.com/api/?lang=python#dashboards**

So I assume the issues with the module  has now been resolved. ))

Now the sample script below now ran without errors
from datadog import initialize, api

options = {
    'api_key': '4e2177053a094d261c10e610b8ca8cdd',
    'app_key': '223159fe496e0c2506af146fa8f0eae896818531'}

	initialize(**options)
	title = 'Average Memory Free Shell 2'
	widgets = [
    	{'definition': {
        	    'type': 'timeseries',
	            'requests': [
        	    {'q': 'avg:system.mem.free{*}'}],
	    'title': 'Average Memory Free'}}]

	layout_type = 'ordered'
	description = 'A dashboard with memory info.'
	is_read_only = True
	notify_list = ['kjo@itadel.dk']

	template_variables = [
    		{'name': 'host1',
     		'prefix': 'host',
     		'default': 'my-host'}]

	api.Dashboard.create(title=title,
        	             widgets=widgets,
                	     layout_type=layout_type,
                     	description=description,
                     	is_read_only=is_read_only,
                     	notify_list=notify_list,
                     	template_variables=template_variables)from datadog import initialize, api


2 Creating Dashboard with 3 widgets 

Having worked around the issue I proceeded to test using the Create a Dashboard endpoint.
I could not easily find how to do the rollup with all the last hour in 1 bucket so I created a widget with rollup applied, 
looked at the json tab and appropriated the request shown below.

	"q": "avg:Up_Down.my_metric{*}.rollup(sum, 3600)",

Based on that I created the “Visualizing Data using Dashboard.py” script seen below.

	from datadog import initialize, api

	options = {'api_key': '4e2177053a094d261c10e610b8ca8cdd',
        	    'app_key': '223159fe496e0c2506af146fa8f0eae896818531'
           	}

	initialize(**options)

	title = "Visualizing Data using Dashboard:"
	widgets = [{
        	    "definition": {
                	            "type": "timeseries",
                        	    "requests": [
                                	        {"q": "avg:Up_Down.my_metric{*}"}
                                        	],
                            	"title": "Custom_Check"
                             	},
            	},
            	{"definition": {
                	            "type": "timeseries",
	                            "requests": [
        	                                {"q": "anomalies(max:mongodb.asserts.userps{*}, 'basic', 5)"}
                	                        ],
                        	    "title": "No of asserts per sec (anomaly detection on)"
	                             },
        	    },
            	{"definition": {
                	            "type": "distribution",
                        	    "requests": [
                                	        {"q": "avg:Up_Down.my_metric{*}.rollup(sum, 3600)"}
	                                        ],
        	                    "title": "Custom_Check with Rollup"
	                            }
	            }]

	layout_type = "ordered"
	description = "3 Widgets."
	is_read_only = True
	notify_list = ["kjo@itadel.dk"]
	template_variables= None

	api.Dashboard.create(title=title,
        	             	widgets=widgets,
                		layout_type=layout_type,
                     		description=description, notify_list=notify_list,
                     		template_variables=template_variables)

3 Take Snapshot

Setting the timeframe to the past 5 minutes was done by zooming in on the graph in the GUI.
I then restarted the Mongodb service waited then stopped if for 30 sec started it and then finally stopped the datadog agent, and then pushed the camera icon and send the snapshot to myself.

Uploaded as "Take a snapshot of this graph.png"

4.	Bonus question What is the Anomaly graph displaying

Looking at: Take a snapshot of this graph.png

The anomaly graph is showing a gray band which is the zone showing the predictive behaviour,  the value must stay within this band 
as to not generate an anomaly.

Where the graph is RED it has thrown up an anomaly. Notice that the anomaly gray band grows when no data is received. 

Also once the backlogged data is reinserted the graphs the anomaly band normalizes as seen in uploaded “Normalised anomaly.png”

So the anomaly function looks at data trend and once a deviation is found it marks the graph for that time period as an anomaly or as the official documentation nicely puts it:

“Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, considering trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.”

Monitoring data:

1. Create new metric monitor

I created the new metric monitor using the GUI
https://app.datadoghq.com/monitors#8524086/edit

Screenshot of the received email for an Alert is uploaded as “Notification_Screenshot.PNG”

2. Bonus question

I created 2 scheduled downtimes I noticed that the notifications where in UTC and the setup showed CET timezones

Uploaded "Downtime_notification_workdays.png"

Collecting APM Data:

1. installation Flask and DD trace
Used instructions at https://app.datadoghq.com/apm/install# 
	pip install ddtrace

Used insttructions at http://flask.pocoo.org/docs/1.0/installation/#install-flask

Installed Flask:
  pip install flask 

Verified versions:
  pip list modules

modified the app.py example file by adding

  from ddtrace import patch_all
  patch_all()

Enabled Flask tracing automatically via ddtrace-run:

  ddtrace-run python app.py

I then generated some traces using

http://localhost:5050/api/trace
http://localhost:5050
http://localhost:5050/api/apm

From the Prompt I could see traces where getting reported in the local console

ddtrace-run python app.py

(venv) C:\temp\venv\Scripts> * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
2019-03-11 00:32:35,659 INFO [werkzeug] [_internal.py:88] -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2019-03-11 00:32:35,659 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2019-03-11 00:33:00,679 INFO [werkzeug] [_internal.py:88] - 127.0.0.1 - - [11/Mar/2019 00:33:00] "GET /api/apm HTTP/1.1" 200 -
2019-03-11 00:33:00,679 - werkzeug - INFO - 127.0.0.1 - - [11/Mar/2019 00:33:00] "GET /api/apm HTTP/1.1" 200 -
2019-03-11 00:33:02,072 DEBUG [ddtrace.api] [api.py:160] - reported 1 traces in 1.00281s
2019-03-11 00:33:02,072 - ddtrace.api - DEBUG - reported 1 traces in 1.00281s

But no Traces arrived at
https://app.datadoghq.com/apm/intro

I then went to the  C:\ProgramData\Datadog\logs\trace-agent.log
And corelated that the error message was created each time I tested with the same message "invalid span"

2019-03-11 00:33:02 ERROR (api.go:249) - dropping trace reason: invalid span (SpanID:4007710452271168478): invalid `Duration`: 0 (debug for more info), [service:"flask" name:"flask.request" r...

At this stage I decided to complete exercise

Uploaded app.py

Final Question:

I would like to create an extension for daikin Air to Air Heatpump. It can be accessed over a REST API. Basically I want to be able to access all my smarthome boxes and sensors. And also see what possibilities there is to monitor a SECOMEA Access Gateway and Gatemanager server.

Its not very creative but its what I could really use at the moment
