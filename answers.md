Your answers to the questions go here.
<br><br>Setup environment:
  <br>https://github.com/DataDog/hiring-engineers/tree/solutions-engineer
  <br>DataDog Demo Setup (14-day trial)
  <br>Be sure to specify “Datadog Recruiting Candidate”
 
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-1-image1.jpg)
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-2-image1.jpg)
 
<p>These instructions are for CentOS/RHEL 6 and above.</p>
<p>Use our easy one-step install.</p>
<p>DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</p>
<p>This will install the YUM packages for the Datadog Agent and will prompt you for your password.<br /> If the Agent is not already installed on your machine and you don't want it to start automatically after the installation, just prepend&nbsp;</p>
<p>DD_INSTALL_ONLY=true</p>
<p>&nbsp;to the above script before running it.</p>
<p>Run:</p>
<p>sudo DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</p>
<p>-&gt; Running transaction check</p>
<p>---&gt; Package datadog-agent.x86_64 1:6.15.1-1 will be installed</p>
<p>--&gt; Finished Dependency Resolution</p>
<p>Dependencies Resolved</p>
<p>================================================================================</p>
<p>&nbsp;Package&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Arch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Repository&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Size</p>
<p>================================================================================</p>
<p>Installing:</p>
<p>&nbsp;datadog-agent&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x86_64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:6.15.1-1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; datadog&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 161 M</p>
<p>&nbsp;</p>
<p>Stop, Start and check status of &nbsp;Datadog Agent using:</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; systemctl start/stop datadog-agent</p>
<p>&nbsp;systemctl status datadog-agent</p>
<p>datadog-agent.service - Datadog Agent</p>
<p>&nbsp;&nbsp; Loaded: loaded (/usr/lib/systemd/system/datadog-agent.service; enabled; vendor preset: disabled)</p>
<p>&nbsp;&nbsp; Active: active (running) since Mon 2019-12-16 20:37:16 EST; 4min 32s ago</p>
<p>&nbsp;Main PID: 5784 (agent)</p>
<br>
<p>&nbsp;</p>
<p><strong><u>Helpful tip for use in the next steps:</u></strong></p>
<p>Validate your agent config in each task below using:</p>
<p>&ldquo;sudo -u dd-agent -- datadog-agent check &lt;your agent name&gt;&rdquo;</p>
<p>&nbsp;</p>
<p><span style="text-decoration: underline;">Example:</span>&nbsp; sudo -u dd-agent -- datadog-agent check elastic</p>
<p>&nbsp;</p>
<p><strong>Data Collection (master agent setup)</strong></p>
<p>&nbsp;</p>
<p style="padding-left: 30px;"><strong><u>Metric Collection Tasks</u></strong></p>
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
Because my laptop gets shutdown frequently, I will create some machines in AWS which will allow continuous data flow.<br>
The default Datadog setup will allow access to numerous AWS services, most with read-only access.<br>
<br><br>
<p>Next setup AWS access for Datadog</p>
 MISSING IMAGE
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
MISSING IMAGE<br>
![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-5-image1.jpg)


<p><strong><u>Helpful tip for use in the next steps:</u></strong></p>
<p>Validate your agent config in each task below using:</p>
<p>&ldquo;sudo -u dd-agent -- datadog-agent check &lt;your agent name&gt;&rdquo;</p>
<p><strong>Example:</strong>&nbsp;sudo -u dd-agent -- datadog-agent check elastic</p>
<p>&nbsp;</p>
<p><strong>Data Collection</strong></p>
<p><strong>&nbsp;</strong></p>
<p><strong><u>&nbsp;</u></strong></p>
<p><strong><u>Metric Collection Tasks</u></strong></p>
<p><strong>Task1</strong></p>
<p>Edit main agent config file:</p>
<p>sudo vi /etc/datadog-agent/datadog.yaml</p>
<p>Add:</p>
<p>hostname: node1.YYYYY.local</p>
<p>tags:</p>
<p>&nbsp; - environment:laptop_vm</p>
<p>&nbsp; - ostype:centos</p>
<p>Uncomment</p>
<p>histogram_aggregates:</p>
<p>&nbsp; - max</p>
<p>&nbsp; - median</p>
<p>&nbsp; - avg</p>
<p>&nbsp; - count</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Observe in Datadog gui</p>
<p>&nbsp;</p>

![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-6-image1.jpg)

