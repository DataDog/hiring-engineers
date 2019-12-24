Your answers to the questions go here.
<br><br>Setup environment:
  <br>https://github.com/DataDog/hiring-engineers/tree/solutions-engineer
  <br>DataDog Demo Setup (14-day trial)
  <br>Be sure to specify “Datadog Recruiting Candidate”
 
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-1-image1.jpg)
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-2-image1.jpg)
 
<p>These instructions are for CentOS/RHEL 6 and above.</p>
<p>Use our easy one-step install.</p>
<p>DD_API_KEY=&lt;my_DatadogAPIKey&gt; bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</p>
<p>This will install the YUM packages for the Datadog Agent and will prompt you for your password.<br /> If the Agent is not already installed on your machine and you don't want it to start automatically after the installation, just prepend&nbsp;</p>
<p>DD_INSTALL_ONLY=true<br>
&nbsp;to the above script before running it.<br>
&nbsp;Run:<br>
&nbsp;sudo DD_API_KEY=&lt;my_DatadogAPIKey&gt; bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</p>
----&gt; Running transaction check<br>
----&gt; Package datadog-agent.x86_64 1:6.15.1-1 will be installed<br>
----&gt; Finished Dependency Resolution<br>
Dependencies Resolved<br>
<p>=============================================================================<br>
&nbsp;Package&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Arch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Repository&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Size<br>
=============================================================================<br>
<p>Installing:<br>
&nbsp;datadog-agent&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x86_64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:6.15.1-1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; datadog&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 161 M</p>
&nbsp;<br>
<p>Stop, Start and check status of &nbsp;Datadog Agent using:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; systemctl start/stop datadog-agent<br>
&nbsp;systemctl status datadog-agent<br>
&nbsp;datadog-agent.service - Datadog Agent<br>
&nbsp;&nbsp; Loaded: loaded (/usr/lib/systemd/system/datadog-agent.service; enabled; vendor preset: disabled)<br>
&nbsp;&nbsp; Active: active (running) since Mon 2019-12-16 20:37:16 EST; 4min 32s ago<br>
&nbsp;Main PID: 5784 (agent)</p>
<br>
<p>&nbsp;</p>
<p><strong><u>Helpful tip for use in the next steps:</u></strong><br>
&nbsp;&nbsp;Validate your agent config in each task below using:<br>
&nbsp;&nbsp;&ldquo;sudo -u dd-agent -- datadog-agent check &lt;your agent name&gt;&rdquo;<br>
&nbsp;</p>
<p><span style="text-decoration: underline;">Example:</span>&nbsp; sudo -u dd-agent -- datadog-agent check elastic</p>
<p>&nbsp;</p>
<strong>Data Collection (master agent setup local laptop vm)</strong><br>
<p style="padding-left: 30px;"><strong><u>Metric Collection Tasks</u></strong><br>
<p style="padding-left: 30px;"><strong>Task1</strong><br>
Edit main agent config file:<br>
sudo vi /etc/datadog-agent/datadog.yaml<br>
Add:<br>
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
CGroup: /system.slice/datadog-agent.service<br>
 └─5784 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/a..<br>
</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Your agent is now reporting to Datadog cloud.&nbsp;<br><br>
<p><span style="text-decoration: underline;"><strong>NOTE</strong></span></p>
Because my laptop gets shutdown frequently, I will create some machines in AWS which will allow continuous data flow.<br>
The default Datadog setup will allow access to numerous AWS services, most with read-only access.<br>
<br><br>
Next setup AWS access for Datadog<br>

 
![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-4-image1.jpg) 

<br>

<p>Connect Datadog to your AWS account to automatically track and tag your EC2 instances, and report on all your Cloudwatch metrics.<br>
Enter AWS credentials for each of your AWS accounts &mdash; you can find them&nbsp;<a href="https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key">here</a>. Note that these credentials only require read-only access to your AWS account.</p>
<br>
<p>Connect to Amazon Web Services (AWS) in order to:</p>
<ul>
<li>See automatic AWS status updates in your stream</li>
<li>Get Cloudwatch metrics for EC2 hosts without installing the Agent</li>
<li>Tag your EC2 hosts with EC2-specific information (e.g. availability zone)</li>
<li>Get Cloudwatch metrics for other services: ELB, RDS, EBS, AutoScaling, DynamoDB, ElastiCache, CloudFront, CloudSearch, Kinesis, Lambda, OpsWorks, Redshift, Route53, SQS, and SNS</li>
<li>See EC2 scheduled maintenance events in your stream</li>
</ul>
<p>&nbsp;</p>
<p>Create linkage from your AWS account to Data Dog AWS account.<br>
Create new role using:</p>
<ul>
<li>Data Dog AWS ID: 464622532012</li>
<li>AWS External ID: &lt;my aws external id&gt;</li>
</ul>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Showing successful initial integration with AWS:</p>

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

<p><strong>Task2: </strong></p>
<p>Install a local database and setup dd-agent to monitor and add tags.<br>
Selected MySQL.<br>
&nbsp;&nbsp;I have run MySQL setup commands to create datadog user with replication and performance metric collection permissions.<br>
<br>
<a href="https://app.datadoghq.com/account/settings#integrations/mysql">Define</a> MySQL user for Datadog agent to utilize<br>
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
<p>Create small MySQL database, repeatedly run a simple query.<br />while true<br />do<br />&nbsp; &nbsp;mysql -uroot --password="" &lt; ~/mysql_query.sql &gt; /dev/null<br />&nbsp; &nbsp;sleep (45)<br />done<br /><br />where file &ldquo;query.sql&rdquo; file contains: &ldquo;select * from datadog.tutorials_tbl;&rdquo;</p>

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

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-11-image1.jpg)
 
 <br>

<br><br>
<p>Bonus: How do you change the agent collection interval?<br>
<a href="https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval">Collection interval</a>
To change the collection interval of your check, use <strong>min_collection_interval</strong> in the configuration file. The default value is 15 which means the check method from your class is invoked with the same interval as the rest of the integrations on the Agent.</p>

<br><br>

<p><span style="text-decoration: underline;">Visualizing Data</span><br>
<strong>Utilize the Datadog API</strong> to create a Timeboard that contains the following visualizations</p>

<p>NOTE:&nbsp;<a href="https://docs.datadoghq.com/getting_started/api/">Datadog recommends using Postman (click here)</a><br>
<p>However, curl is a suitable alternative noted.&nbsp;<a href="https://www.datadoghq.com/blog/programmatically-manage-your-datadog-integrations/">Curl skeleton examples (click here)</a><br>
&nbsp;&nbsp;and<br>
<a href="https://docs.datadoghq.com/api/?lang=bash#comments">https://docs.datadoghq.com/api/?lang=bash#comments</a></p>
<br>
Instructions:<br>
<p>Utilize the Datadog API to create a Timeboard that contains:</p>
<ul>
<li>Your custom metric scoped over your host.</li>
<li>Any metric from the Integration on your Database with the anomaly function applied.</li>
<li>Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket</li>
</ul>
<p>&nbsp;</p>
<p>Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.</p>
<p>Once this is created, access the Dashboard from your Dashboard List in the UI:</p>
<ul>
<li>Set the Timeboard's timeframe to the past 5 minutes</li>
<li>Take a snapshot of this graph and use the @ notation to send it to yourself.</li>
<li><strong>Bonus Question</strong>: What is the Anomaly graph displaying?</li>
</ul>
<p style="padding-left: 30px;">The Anomaly graph is displaying &ldquo;anomalies(avg:mysql.performance.queries{host:aws.YYYYY.localdomain},'basic',2)&rdquo;</p>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg12-image1.jpg)
 
<br>
<br>
<br>

<p><strong>My API Create procedure used:</strong></p>
<ul>
<li>Created dashboard in Datadog GUI first.</li>
</ul>
<p>It&rsquo;s easier to use a gui to build the desired visualizations, then export as json, and edit the json as desired.</p>
<ul>
<li>Once exported as json it is one single line.</li>
<li>Install Linux tool &ldquo;jq&rdquo; to format the single json line into human readable multi-line json</li>
</ul>
&nbsp;&nbsp;<p><strong>RUN: cat SavedSingleLineDashboardJsonFile.json | jq . &gt; HumanReadableJson.json</strong></p>
<ul>
<li>Edit file &ldquo;HumanReadableJson.json &ldquo; appropriately to specify custom values and remove attributes like &ldquo;id&rdquo;</li>
<li>Create curl script as shown with API_KEY and APP_KEY</li>
</ul>
<p>See reference: <a href="https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard">https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard</a></p>
<ul>
<li>Ran Curl script as shown (sh ./scriptName) :</li>
</ul>
<p><strong>Example skeleton curl command:</strong><br>
api_key=b18a088feb147e7535796e62ad33fc42<br>
app_key=97b83f906689b65bbd10e57f60529c56d539947e<br>
curl&nbsp; -X POST \<br>
-H "Content-type: application/json" \<br>
-H "DD-API-KEY: ${api_key}" \<br>
-H "DD-APPLICATION-KEY: ${app_key}" \<br>
-d '{<br>
&nbsp;&nbsp;&nbsp;&nbsp; &lt;&lt;&lt;&lt; dashboard json goes here &gt;&gt;&gt;&gt;<br>
<p>}' \<br>
"https://api.datadoghq.com/api/v1/dashboard"</p>
<br>
