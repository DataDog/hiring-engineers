Your answers to the questions go here.
<br><br>Setup environment:
  <br>https://github.com/DataDog/hiring-engineers/tree/solutions-engineer
  <br>DataDog Demo Setup (14-day trial)
  <br>Be sure to specify “Datadog Recruiting Candidate”
 
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-1-image1.jpg)
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-2-image1.jpg)
 
These instructions are for CentOS/RHEL 6 and above.<br>
Use our easy one-step install.<br>
DD_API_KEY=&lt;my_DatadogAPIKey&gt; bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"<br><br>
This will install the YUM packages for the Datadog Agent and will prompt you for your password. If the Agent is not already installed on your machine and you don't want it to start automatically after the installation, just prepend DD_INSTALL_ONLY=true to the above script before running it.<br>
<br>
&nbsp;Run:<br>
&nbsp;sudo DD_API_KEY=&lt;my_DatadogAPIKey&gt; bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"<br>
----&gt; Running transaction check<br>
----&gt; Package datadog-agent.x86_64 1:6.15.1-1 will be installed<br>
----&gt; Finished Dependency Resolution<br>
Dependencies Resolved<br>
=============================================================================<br>
&nbsp;Package&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Arch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Repository&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Size<br>
=============================================================================<br>
Installing:<br>
&nbsp;datadog-agent&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x86_64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:6.15.1-1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; datadog&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 161 M</p>
&nbsp;<br>
Stop, Start and check status of &nbsp;Datadog Agent using:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sudo systemctl start/stop datadog-agent<br><br>
&nbsp;sudo systemctl status datadog-agent<br>
&nbsp;datadog-agent.service - Datadog Agent<br>
&nbsp;&nbsp; Loaded: loaded (/usr/lib/systemd/system/datadog-agent.service; enabled; vendor preset: disabled)<br>
&nbsp;&nbsp; Active: active (running) since Mon 2019-12-16 20:37:16 EST; 4min 32s ago<br>
&nbsp;Main PID: 5784 (agent)<br>
<br>

<br>
<strong><u>Helpful tip for use in the next steps:</u></strong><br>
&nbsp;&nbsp;Validate your agent config in each task below using:<br>
&nbsp;&nbsp;&ldquo;sudo -u dd-agent -- datadog-agent check &lt;your agent name&gt;&rdquo;<br>

<hr>
<strong>Example:</strong>&nbsp; sudo -u dd-agent -- datadog-agent check elastic<hr>
<hr>

<strong>Data Collection</strong> (master agent setup done on local laptop vm)<br>
Metric Collection Tasks<br>
<p style="padding-left: 30px;"><strong>Task1</strong><br>
Edit main agent config file:<br>
sudo vi /etc/datadog-agent/datadog.yaml<br>
Add:<br><br><br>
hostname: node1.YYYYY.local<br>
tags:<br>
- environment:laptop_vm<br>
- ostype:centos<br>
Uncomment<br>
<histogram_aggregates:<br>
- max<br>
- median<br>
- avg<br>
- count<br>
</p>
<p>Observe results in Datadog gui<br>
<br>
sudo systemctl restart datadog-agent<br>
CGroup: /system.slice/datadog-agent.service<br>
 └─5784 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/a..<br>
</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Your agent is now reporting to Datadog cloud.&nbsp;<br><br>
<strong>NOTE</strong></span><br>
Because my laptop gets shutdown frequently, I will create some machines in AWS which will allow continuous data flow.<br>
The default Datadog setup will allow access to numerous AWS services, most with read-only access.<br>
<br><br>
Next setup AWS access for Datadog<br>

 
![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-4-image1.jpg) 

<br>

Connect Datadog to your AWS account to automatically track and tag your EC2 instances, and report on all your Cloudwatch metrics.<br>
Enter AWS credentials for each of your AWS accounts &mdash; you can find them&nbsp;<a href="https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key">here</a>. Note that these credentials only require read-only access to your AWS account.<br>
<br>
Connect to Amazon Web Services (AWS) in order to:<br>
<ul>
<li>See automatic AWS status updates in your stream</li>
<li>Get Cloudwatch metrics for EC2 hosts without installing the Agent</li>
<li>Tag your EC2 hosts with EC2-specific information (e.g. availability zone)</li>
<li>Get Cloudwatch metrics for other services: ELB, RDS, EBS, AutoScaling, DynamoDB, ElastiCache, CloudFront, CloudSearch, Kinesis, Lambda, OpsWorks, Redshift, Route53, SQS, and SNS</li>
<li>See EC2 scheduled maintenance events in your stream</li>
</ul>

<p>Create linkage from your AWS account to Data Dog AWS account.<br>
Create new role using:</p>
<ul>
<li>Data Dog AWS ID: 464622532012</li>
<li>AWS External ID: &lt;my aws external id&gt;</li>
</ul>

Showing successful initial integration with AWS:<br>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-5-image1.jpg)


<p><strong><u>Helpful tip for use in the next steps:</u></strong><br>
Validate your agent config in each task below using:<br>
&ldquo;sudo -u dd-agent -- datadog-agent check &lt;your agent name&gt;&rdquo;<br>
<strong>Example:</strong>&nbsp;sudo -u dd-agent -- datadog-agent check elastic<br>
<p>&nbsp;</p>
<p><strong>Data Collection (master agent AWS machine)</strong><br>
<strong><u>Metric Collection Tasks</u></strong><br>
<p><strong>Task1</strong><br>
Edit main agent config file:<br>
&nbsp;&nbsp;sudo vi /etc/datadog-agent/datadog.yaml<br>
&nbsp;Add:<br>
&nbsp;&nbsp;&nbsp;hostname: node1.YYYYY.local<br>
<p>tags:<br>
&nbsp; - environment:AWS_vm<br>
&nbsp; - ostype:centos<br>
&nbsp;Uncomment<br>
&nbsp;histogram_aggregates:<br>
&nbsp;&nbsp; - max<br>
&nbsp;&nbsp; - median<br>
&nbsp;&nbsp; - avg<br>
&nbsp;&nbsp; - count<br>
&nbsp;<br>
&nbsp;<br>
  </p>
Observe collected data in Datadog gui<br>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-6-image1.jpg)

<strong>Task2: </strong>
Install a local database and setup Datadog agent to monitor and add tags. I selected MySQL.<br>
There are MySQL setup commands to create datadog user with replication and performance metric collection permissions.<br>
<br>
<a href="https://app.datadoghq.com/account/settings#integrations/mysql">Setup MySQL user for Datadog agent to utilize (click here)</a><br>
Then edit file /etc/datadog-agent/conf.d/mysql.d/conf.yaml to contain the credentials, tags and optionally any custom queries to perform.<br>
&nbsp;&nbsp;Example:<br>
&nbsp;&nbsp;init_config:<br>
<br>
&nbsp;&nbsp;instances:<br>
&nbsp;&nbsp; - server: 127.0.0.1<br>
&nbsp;&nbsp;&nbsp; user: datadog<br>
&nbsp;&nbsp;&nbsp;&nbsp; pass: datadog<br>
&nbsp;&nbsp;&nbsp; port: 3306<br>
&nbsp;&nbsp;&nbsp; options:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; replication: false<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; galera_cluster: true<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; extra_status_metrics: true<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; extra_innodb_metrics: true<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; extra_performance_metrics: true<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; schema_size_metrics: false<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; disable_innodb_metrics: false<br>
<br>
&nbsp;&nbsp; logs:<br>
&nbsp;&nbsp;&nbsp; - type: file<br>
&nbsp;&nbsp;&nbsp;&nbsp; path: /opt/mysql/logs/node1.local.err<br>
&nbsp;&nbsp;&nbsp;&nbsp; source: mysql<br>
&nbsp;&nbsp;&nbsp;&nbsp; sourcecategory: database<br>
&nbsp;&nbsp;&nbsp;&nbsp; service: mysql<br>
<br>
&nbsp;&nbsp;tags:<br>
&nbsp;&nbsp;&nbsp; - BillYYYY:Mysql_VM<br>
&nbsp;&nbsp;&nbsp; - OSType:CentOS<br>


<p>Extra setup step:<br>
To generate MySQL load for graphing purposes:<br>
Open Linx Screen window, create small MySQL database, repeatedly run a simple query.<br />while true<br />do<br />&nbsp; &nbsp;mysql -uroot --password="" &lt; ~/mysql_query.sql &gt; /dev/null<br />&nbsp; &nbsp;sleep (45)<br />done<br /><br />where file &ldquo;query.sql&rdquo; file contains: &ldquo;select * from datadog.tutorials_tbl;&rdquo;<br>

<p>Once the agent is operational, be sure to add the pre-built MySQL dashboards located under &ldquo;Integrations&rdquo;</p>


![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-9-image1.jpg)

<br>
<p> Observe collected data</p>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-9-image2.jpg)

<br>
<p><strong>Task3: </strong></p><br>
<p>References<br>
<a href="https://dbader.org/blog/monitoring-your-nodejs-app-with-datadog">https://dbader.org/blog/monitoring-your-nodejs-app-with-datadog</a><br>
<a href="https://github.com/dbader/node-datadog-metrics">https://github.com/dbader/node-datadog-metrics</a><br>
<br>
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.<br>
Reference <a href="https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7">Here</a><br>
<br>
<p>&nbsp; &nbsp; <strong>My python my_metric script</strong></p>
&nbsp;&nbsp;from datadog import initialize, statsd<br>
&nbsp;&nbsp;import time,random<br>
&nbsp;&nbsp;from random import *<br>
&nbsp;&nbsp;options = {<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'statsd_host':'127.0.0.1',<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'statsd_port':8125<br>
&nbsp;&nbsp;}<br>
&nbsp;&nbsp;initialize(**options)<br>
&nbsp;&nbsp;i=0<br>
&nbsp;&nbsp;while(1):<br>
&nbsp;&nbsp;&nbsp; i += 1<br>
&nbsp;&nbsp;&nbsp; x=randint(1, 1000)<br>
&nbsp;&nbsp;&nbsp; statsd.gauge('my_metric.gauge', x, tags=["environment:my_metric"])<br>
&nbsp;&nbsp;&nbsp; print("i=",i," x=",x)<br>
&nbsp;&nbsp;&nbsp; time.sleep(10)<br>
<br>
<p>The names of the configuration and check files must match. If your check is called mycheck.py, your configuration file must be named mycheck.yaml.</p>


![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-10-image1.jpg)

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/my_metric.jpg)
 
 <br>
<p>Bonus: <br>How do you change the agent collection interval?<br>
<a href="https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval">Collection interval</a>
To change the collection interval of your check, use <strong>min_collection_interval</strong> in the configuration file. The default value is 15 which means the check method from your class is invoked with the same interval as the rest of the integrations on the Agent.</p>

<br><br>

<strong><underline>Visualizing Data</underline></strong><br>
<strong>Utilize the Datadog API</strong> to create a Timeboard that contains the following visualizations<br>
<br>

NOTE:&nbsp;<a href="https://docs.datadoghq.com/getting_started/api/">Datadog recommends using Postman (click here)</a><br>
Curl is a suitable alternative noted here: &nbsp;<a href="https://www.datadoghq.com/blog/programmatically-manage-your-datadog-integrations/">API examples (click here)</a>&nbsp;&nbsp;and<br>
<a href="https://docs.datadoghq.com/api/?lang=bash#comments">Curl Examples (click here)</a><br>
<br>
Utilize the Datadog API to create a Timeboard that contains:<br>
<ul>
<li>Your custom metric scoped over your host.</li>
<li>Any metric from the Integration on your Database with the anomaly function applied.</li>
<li>Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket</li>
</ul>
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.<br>
Once this is created, access the Dashboard from your Dashboard List in the UI:<br>
<ul>
<li>Set the Timeboard's timeframe to the past 5 minutes</li>
<li>Take a snapshot of this graph and use the @ notation to send it to yourself.</li>
<li><strong>Bonus Question</strong>: What is the Anomaly graph displaying?</li>
</ul>
<p style="padding-left: 30px;"><strong>Answer:</strong> The Anomaly graph is displaying &ldquo;anomalies(avg:mysql.performance.queries{host:aws.YYYYY.localdomain},'basic',2)&rdquo;</p>

<br>
<br>
For most, it&rsquo;s easier to use a gui to build the desired visualizations, then export as json, and edit the json as desired.<br>
Started with this visualization<br>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg12-image1.jpg)
 
<br>
<br>
<br>

<strong>The API Create procedure used:</strong><br>
<ul>
<li>Created dashboard in Datadog GUI first.</li>
</ul>
<ul>
<li>Once exported as json it is one single line.</li>
<li>Install Linux tool &ldquo;jq&rdquo; to format the single json line into human readable multi-line json</li>
</ul>
&nbsp;&nbsp;<strong>RUN: cat SavedSingleLineDashboardJsonFile.json | jq . &gt; HumanReadableJson.json</strong><br>
<ul>
<li>Edit file &ldquo;HumanReadableJson.json &ldquo; appropriately to specify custom values and remove attributes like &ldquo;id&rdquo;</li>
<li>Create curl script as shown with API_KEY and APP_KEY</li>
</ul>
<p>See reference: <a href="https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard">https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard</a></p>
<br>
<strong>Here is an example curl command:</strong><br>
api_key=&lt;my_DatadogAPIKey&gt;<br>
app_key=&lt;my_DatadogAPPKey&gt;<br>
curl&nbsp; -X POST \<br>
-H "Content-type: application/json" \<br>
-H "DD-API-KEY: ${api_key}" \<br>
-H "DD-APPLICATION-KEY: ${app_key}" \<br>
-d '{<br>
&nbsp;&nbsp;&nbsp;&nbsp; &lt;&lt;&lt;&lt; dashboard json goes here &gt;&gt;&gt;&gt;<br>
<p>}' \ <br>
"https://api.datadoghq.com/api/v1/dashboard"</p>
<br>
<br>
<br>
<strong>Specific curl script used:</strong><br>
<ul>
  <li>&nbsp;&nbsp;Ran Curl script as shown <strong> sh ./scriptName </strong></li>
</ul>
<p>Calling out the lines which show filtering per hostname are:<br>
&nbsp;&ldquo;<strong> q": "sum:my_metric.gauge{host:aws.YYYYY.localdomain} by {host}.rollup(sum), 3600",</strong><br>
&nbsp;&ldquo;<strong> q": "max:mysql.performance.queries{host:aws.YYYYY.localdomain} by {host}" &ldquo;</strong></p>
<p>&nbsp;</p>
<p>Here is my curl script showing it is specifically filtered on my AWS host.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>- ----Curl script ---- </strong><br>
api_key=&lt;my_DatadogAPIKey&gt;<br>
app_key=&lt;my_DatadogAPPKey&gt;<br>
<p>&nbsp;</p>
<p>curl&nbsp; -X POST \<br>
-H "Content-type: application/json" \<br>
-H "DD-API-KEY: ${api_key}" \<br>
-H "DD-APPLICATION-KEY: ${app_key}" \<br>
-d '<br>
{<br>
&nbsp; "title": "Using CURL Created Bill YYYYY Timeboard with AWS Spend",<br>
&nbsp; "description": "Used Curl to create",<br>
&nbsp; "widgets": [<br>
&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "definition": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "type": "timeseries",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "requests": [<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "q": "sum:my_metric.gauge{host:aws.YYYYYY.localdomain} by {host}.rollup(sum), 3600",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "display_type": "line",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "style": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "palette": "dog_classic",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_type": "solid",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_width": "normal"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ],<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "title": "Using CURL Created Sum of&nbsp; last hour \"my_metric\" values: aws.YYYYYY.localdomain",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "show_legend": false,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "legend_size": "0"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp; },<br>
&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "definition": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "type": "timeseries",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "requests": [<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;<strong>"q": "max:mysql.performance.queries{host:aws.YYYYY.localdomain} by {host}",</strong><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "display_type": "area",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "style": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "palette": "dog_classic",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_type": "solid",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_width": "normal"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; },<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "q": "max:system.load.1{host:aws.YYYYY.localdomain} by {host}",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "display_type": "area",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "style": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "palette": "dog_classic",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_type": "solid",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_width": "normal"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; },<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>"q": "max:mysql.performance.com_select{host:aws.YYYYY.localdomain} by {host}",</strong><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "display_type": "line",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "style": {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "palette": "dog_classic",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_type": "solid",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "line_width": "normal"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ],<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "title": "Using CURL created MySQL&nbsp; performance vs MySQL query performance vs. 1min system load",<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "show_legend": false,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "legend_size": "0"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }</p>

<ul>
  <li>Results running Curl script as shown <strong> RUN:  sh ./scriptName </strong></li>
</ul>


![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-16-image1.jpg)
 
 
<br>
<p><strong>Monitoring Data</strong></p>
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:<br>
•	Warning threshold of 500<br>
•	Alerting threshold of 800<br>
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.<br><br>
Please configure the monitor’s message so that it will:
•	Send you an email whenever the monitor triggers.<br>
•	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.<br>
•	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.<br>
•	When this monitor sends you an email notification, take a screenshot of the email that it sends you.<br><br><br>
•	Bonus Question: <br>Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:<br>
o	One that silences it from 7pm to 9am daily on M-F,<br>
o	And one that silences it all day on Sat-Sun.<br>
o	Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.<br>
