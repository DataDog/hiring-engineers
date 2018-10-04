<p>
<h1>Collecting Metrics:</h1>

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<br><b>Solution:</b></br>
Assigned tags using the configuration file following the instruction <a href="https://docs.datadoghq.com/tagging/assigning_tags/#assigning-tags-using-the-configuration-files">here.</a>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44914740032/in/dateposted-public/" title="host tag">
<img src="https://farm2.staticflickr.com/1936/44914740032_7045ae6a56_o_d.png"></a>

<p>
2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
<br><b>Solution:</b></br>
Installed MySQL on the virtual machine and then installed MySQL integration following the instructions <a href="https://docs.datadoghq.com/integrations/mysql/#prepare-mysql">here.</a>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/30027050007/in/dateposted-public/" title="MySQL - overview">
<img src="https://farm2.staticflickr.com/1973/30027050007_f6ceea71d5_o_d.png"></a>

<p>
3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
<br><b>Solution:</b></br>
Created a file called mycheck.yaml with the following content in /etc/datadog-agent/conf.d

<pre><code>
init_config:

instances:
   [{}]

</code></pre>

<p>
Then created a file called mycheck.py in /etc/datadog-agent/checks.d with the following content:

<pre><code>
__version__ = "1.0.0"
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,1000))

</code></pre>

<p>
And then restarted the datadog-agent; the metric was being reported at the default interval - 20 seconds.

<p>
<a href="https://www.flickr.com/photos/144323826@N02/30134298117/in/dateposted-public/" title="my_metric">
<img src="https://farm2.staticflickr.com/1917/30134298117_c6886e8a55_o_d.png"></a>

<p>
4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

<br><b>Solution:</b></br>
Modified mycheck.yaml in /etc/datadog-agent/conf.d as below:

<pre><code>
init_config:

instances:
   - min_collection_interval: 45

</code></pre>

<p>
And then restarted the datadog-agent. The metric was being reported at 60 seconds interval afterwards - the explanation is <a href="https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6#configuration">here.</a>


<h1>Visualizing Data:</h1>

Utilize the Datadog API to create a Timeboard that contains:
<li>Your custom metric scoped over your host.</li>
<li>Any metric from the Integration on your Database with the anomaly function applied.</li>
<li>Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.</li>

<br><b>Solution:</b></br>
I have used the following python script to create the timeboard

<p>
<pre><code>
from datadog import initialize, api

options = {
    'api_key': 'e2153221b4caadb8f04b1a973d901dd2',
    'app_key': 'c002b47fde144736c6674e163a84dc7a35c3f467'
}

initialize(**options)

title = "Timeboard 3 - Custom metric scoped over ashif.com"
description = "Visualizing Data - Task 1"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Customer Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:system.cpu.idle{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average CPU Idle reported by MySQL Dashboard"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Customer Metric Rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ashif.com"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
					 

</code></pre>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44351019334/in/dateposted-public/" title="timeboard">
<img src="https://farm2.staticflickr.com/1960/44351019334_5e776c1586_o_d.png"></a>

<p>
Once this is created, access the Dashboard from your Dashboard List in the UI:
<li>Set the Timeboard's timeframe to the past 5 minutes.</li>
<li>Take a snapshot of this graph and use the @ notation to send it to yourself.</li>

<p>
Then I accessed the timeboard using the web UI, dragged the mouse over the graph for "Average CPU Idle reported by MySQL Dashboard" to zoom in and set the Timeboard's timeframe to the past 5 minutes. Then I clicked on the camera icon to take a snapshot and used the @ notation to send the snapshot to myself.

The following the screenshot of the snapshot which was emailed to me as a result.

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44160594805/in/dateposted-public/" title="snapshot email">
<img src="https://farm2.staticflickr.com/1974/44160594805_f849386ddb_o_d.png"></a>

<p>
Bonus Question: What is the Anomaly graph displaying?
<br><b>Solution:</b></br>
In the graph, the anomaly function has detected a pattern where the cpu was not that idle (which is usually not the case) because that was the time when I ran some mysql stress test to stree out the cpu using 'mysqlslap'. The CPU in my VM is usually 100% idle and running 'mysqlslap' stress test made the cpu to go up - the anomaly function caught that up.


<h1>Monitoring Data:</h1>

<p>
When the configured monitor sends you an email notification, take a screenshot of the email that it sends you.
<br><b>Solution:</b></br>

The following are the screenshots of alert email notification:

<p>
<a href="https://www.flickr.com/photos/144323826@N02/45070819681/in/dateposted-public/" title="alert email - warning">
<img src="https://farm2.staticflickr.com/1977/45070819681_7d3bc6b8c1_o_d.png"></a>


<p>
<a href="https://www.flickr.com/photos/144323826@N02/30134298937/in/dateposted-public/" title="alert email - warning">
<img src="https://farm2.staticflickr.com/1948/30134298937_2deb9f14e7_o_d.png"></a>

<p>
And I had the following in "Say what's happening" section while configuring the monitor:

<pre><code>
my_metric alert on {{host.name}}

Hello there,

my_metric has just triggered this alert on host {{host.ip}}.

{{#is_alert}}
The metric average is above {{threshold}} for the last 5 minutes. The metric value at the time the alert triggered is {{value}}.
{{/is_alert}}

{{#is_warning}}
The metric average is above {{warn_threshold}} for the last 5 minutes. The metric value at the time the warning triggered is {{value}}.
{{/is_warning}}

{{#is_no_data}}
The metric didn't report any values for the last 10 minutes.
{{/is_no_data}}

Notify: @ashifiqbal@yahoo.com 
</code></pre>

<p>
Bonus Question: Make sure that your email is notified when you schedule the downtime (One that silences it from 7pm to 9am daily on M-F and one that silences it all day on Sat-Sun.) and take a screenshot of that notification.
<br><b>Solution:</b></br>
The following are the screenshots:

<p>
<a href="https://www.flickr.com/photos/144323826@N02/30134299327/in/dateposted-public/" title="alert downtime schedule - monday to friday">
<img src="https://farm2.staticflickr.com/1909/30134299327_164daae30b_o_d.png"></a>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/30134299797/in/dateposted-public/" title="alert downtime email - monday to friday">
<img src="https://farm2.staticflickr.com/1921/30134299797_8368eca0bc_o_d.png"></a>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44351020274/in/dateposted-public/" title="alert downtime schedule - saturday sunday">
<img src="https://farm2.staticflickr.com/1954/44351020274_521ca81658_o_d.png"></a>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44351020444/in/dateposted-public/" title="alert downtime email - saturday sunday">
<img src="https://farm2.staticflickr.com/1971/44351020444_e6977aa2a3_o_d.png"></a>

<h1>Collecting APM Data:</h1>
<p>
Instrument a python app using Datadog’s APM solution:
<br><b>Solution:</b></br>
<p>
I have used the following python code - the file was saved as primetest.py and I have used the following command to collect APM data.

<p>
<code>ddtrace-run python primetest.py</code>

<pre><code>
# primetest.py
from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def prime_num():
	num = random.randint(1,100000)

	# prime numbers are greater than 1
	if num > 1:
	   # check for factors
	   for i in range(2,num):
		   if (num % i) == 0:
			   output = "Random number %d is not a prime number." % num
			   break
	   else:
		   output = "Random number %d is a prime number." % num

	# if input number is less than
	# or equal to 1, it is not prime
	else:
	   output = "Random number %d is not a prime number." % num

	return output

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5100')

</code></pre>

<p>
Screenshot of a Dashboard with both APM and Infrastructure Metrics:

<p>
Link: 
<code>https://p.datadoghq.com/sb/b6236c47e-2512a5a2d712a3b3fc3a0cf15ebc0843</code>

<p>
<a href="https://www.flickr.com/photos/144323826@N02/44351019854/in/dateposted-public/" title="dashboard">
<img src="https://farm2.staticflickr.com/1954/44351019854_8813585812_o_d.png"></a>

<p>
Bonus Question: What is the difference between a Service and a Resource?

<br><b>Solution:</b></br>

<b>Service</b>
<br />
A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service.

<br />
<b>Resource</b>
<br />
A particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?

<p>
More information on these <a href="https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-">here.</a>

