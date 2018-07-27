# answers.md



**Table of Contents**

[TOC]
# Setup environment
I opted to use AWS as my environment.  I used a generic Amazon Linux 2 AMI.  Initially, opted for a micro-sized instance, but then ran into memory issues when trying to install something with which to integrate with Datadog.  In retrospect, I wish I could buy back my setup time at a rate $.04 an hour.  At least I was able to see what >1 host looks like on the DD dashboard.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+00.png)

**Figure 0.**  Amazon EC2 Linux 2 AMI 

# Install DD agent
On the initial micro- instance, I used the simple installation method for Agent v6.  The second go-around on my medium- instance I followed the manual setup steps for Agent v6 also.  I understand the components a bit better after doing so and would probably opt for manual installation steps going forward since they are actually very straightforward.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+01.png)

**Figure 1.** Shows installation status after using the all-in-one installation command.  Using DD_INSTALL_ONLY to before manually starting up the service using `systemctl`

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+02.png)

**Figure 2.** DD agent confirmed reporting.  Host shown in dashboard in next section – #Add host tags

# Add host tags

NOTE: Documentation could use some additional clarification here.  The tags were not updating for me and I was unsure to the causation as to why…: was I was saving in the wrong directory?, making incorrect modifications to the yaml file?, or something else?  I updated the .yaml in the conf.d/ directory but I did not see the tags appear in the dashboard.  Luckily, I was able to use the API and use the commands:

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+03.png)

**Figure 3.** Created an APP Key to use API

GET https://api.datadoghq.com/api/v1/hosts?api_key=9bac00822281eda0fc66f5f013abfe17&application_key=e13da5f9b95a9f292b86d50a1a03d62dc35c053d – There are my hosts and their info
GET https://api.datadoghq.com/api/v1/tags/hosts - To verify it wasn’t a page-refresh problem, but the tags were genuinely not being recognized from my monitoring agent.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+04.png)

**Figure 4.** Verifying that no tags

POST https://api.datadoghq.com/api/v1/tags/hosts/i-054c15f0a3f828a58?api_key=9bac00822281eda0fc66f5f013abfe17&application_key=e13da5f9b95a9f292b86d50a1a03d62dc35c053d

Body (application/json):
`{
	"host":"i-054c15f0a3f828a58",
	"tags": [
		"color:grey",
		"size:t2_medium",
		"env:prod",
		"region:west_2c"
	]
}
`
![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+05.png)

**Figure 5.** OK – cool we now have some tags that belong to the host.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+06.png)

**Figure 6.** A green host and a grey host. (Here they are Filtered by their color tags)
(Sorry, I don't know why I picked these two colors instead of something like "red" and "blue".)

# Create custom agent check
I followed the documentation within the DD Developer Tools “Writing An Agent Check” (referred to in the exercise references).
I created a .py file for my check and a .yaml file for my config.
There is a lot of power to create some very elaborate check scripts with python here, however the random metric is very simple.  I can imagine that the HTTP request example would be quite common in the case of hitting public endpoints for monitoring (however I’m not sure of the incentives/economics behind the tradeoff between more comprehensive monitors and high numbers of deployed monitors for customer cases – or if that is even a valid issue). 
NOTE: I did not know how long to wait before my gauged metrics would start showing up.  I must’ve gone back and forth, refreshed pages, and restarted a dozen times before frustratingly going back to the manual only to find that the metrics were being collected all the while.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+07.png)

**Figure 7.** I believe this is the final save of my check script.  It runs.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+08.png)

**Figure 8.** View from metrics explorer

# Collect custom metric
Custom metrics are collected as noted in **Figures 8** and **9**.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+09.png)
**Figure 9.** A day later, the Doug Metric has reliably returned unreliable data.

#Collect integration metric
Opted for PostgreSQL integration.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+10.png)

**Figure 10.** Showing final step of Postgres integration installed

Installed postgres onto the box and followed the instructions to complete the integration from the web portal.  Straightforward install and communication setup.  To confirm I asked for a verbose status from the command line; see status info confirming metrics are being collected from the integration below in Figure 11:

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+11.png)

**Figure 11.** Posgres metrics observed being sent from Service status of DataDog agent

# AWS Integration (Bonus integration)

Since I terminated my instance in AWS prior to leaving for my vacation, I re-installed the agent to continue the second half of the exercise (APM).  However, when adding the host, a video on youtube inspired me to look into the AWS integration since I could essentially see all of my hosts from within Datadog.
As a newcomer to Datadog the instructions for the setup of the AWS integration was not as straightforward as the youtube video had led me.  I had 5-6 tabs open between Datadog and AWS to first determine appropriate AWS security policies, roles, and then subsequently which ID’s and keys belonged to the correct fields.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+12.png)

**Figure 12.** Confirming account credentials are valid for integration!

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+13.png)

**Figure 13.** Make sure you scroll down to “Install Integration”, otherwise you will need to recreate your security policy with a new AWS external ID that Datadog auto-generates in this form!

# Modify collection interval

To modify the collection interval without modifying the .py check file, this can be done in the configuration .yaml file by adding key pair `“-min_collection_interval:45”` under Instances; therefore, the service does not need to be restarted.  Refer to screenshot of **Figure 7**.

# Create timeboard

In the UI I created a timeboard under “Dashboards” and left the default name: “DOUG's Timeboard 8 Jul 2018 22:52”.  I added the average of my random metric over time, selecting it from the dropdown.  If I were to plot the integration metric, I would do so the same way.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+14.png)

**Figure 14.** Timeboard of average value of my random check return

There is a specific question in the instructions asking for a script - I simply followed the Dashboard setup in the UI, I did a search on functions and queries hoping to find more resources.  I work with Grafana panels a lot and it appears to function in a similar manner.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+15.png)

**Figure 15.** This is an interesting metric view (of a random range) showing the absolute value of the difference between returned values.  This gives occasional high peaks in its behavior.

# Anomaly graph

Using the logic from **Figure 13** (above).  “Nicer”/ more rare anomalies can be selected from this random output.  Datadog appears to expect a normal (grey band) range of results based on a rolling evaluation window.  This can be good to identify deviations from an expected pattern (e.g. daily usage patterns).

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+16.png)

**Figure 16.** This is an interesting metric view (of a random range) showing the absolute value of the difference between returned values.  This gives occasional high peaks in its behavior.

# Alert threshold definitions

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+17.png)

**Figure 17.** Alert above metrics returned in last 5 minutes >800, alert >500, and notify if data missing >10 minutes

# Alert email configurations

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+18.png)

**Figure 18.** Using variables, emails are defined for the alerts.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+19.png)

**Figure 19.** An email showing the alert

# Define exclusion period

Following the instructions, I defined an exclusion period for evenings and weekends for the monitor defined in previous steps.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+20.png)

**Figure 20.**  Exclusion period showing 48 hour period of weekend time

# Collecting APM data

Installed the ddtrace client onto the instance per the instructions and deployed the Flask app to be run and trigger trace metrics.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+21.png)

**Figure 21.** Compared to a setup with AppDynamics this was slightly more unpredictable as I spent a lot of time on the above figure screen waiting for my traces to become available.

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+22.png)

**Figure 22.** vi editor showing myapp.py including the trace middleware to track request timings and templates

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+23.png)

**Figure 23.** Running the application with ddtrace will enable logging / trace capture

![](https://s3-us-west-2.amazonaws.com/dougdatadog/Figure+24.png)

**Figure 24.** Trace metrics can be pulled into dashboard objects.  Note: This is a simple dashboard that I recreated after launching a second EC2 instance (missing first half of exercise, tags, etc. after I terminated the first instance going on week vacation).

# Bonus question (service vs resource)

Business applications can consist of many services and each of those services can contain many more resources. 
A service is a set of processes that provide functions to an application.  APM can trace transactions through several services of an application (e.g. web, db, etc).
A service is comprised of many unique resources.  Resources can be discretely unique or grouped for the service they are used within.

# Final question
After a very brief probe into this exercise familiarizing myself with DD, I have recognized a ton of use cases at my current monitoring and testing customers + prospects.

1.	Specifc example - US automakers are behind the times and playing catch-up with automotive telematics (perhaps with the exception of Tesla).  US automakers include even popular European and Japanese brands since the North American market is defined apart from other regions.  API’s providing registration, safety services, keyless entry, service + maintenance, etc. are amalgamated across new and legacy systems.  The inertia (internally within these orgs) and ease of implemeting DD agent monitoring agents in the new telematics hosts is a great opportunity, as well as expansion into the huge forest of legacy systems.

2.	General example - Monitoring groups at large orgs are often tasked with simply “monitoring” their business-critical infrastructure and applications (with less focus on nuances of what, where, why, how).  The larger the footprint of the solution, the less risk these groups need to assume in acquisition, training, and maintenance/upkeep.  Seems ideal for a solution like DD.

3. Creative example - I was genuinely impressed by the extent possible to create custom agent checks.  Pretty much anything that you can script can be monitored!  I think I breifly mentioned the following on a call with either Fahim or Boyan: This is a great "ace in the hole" for potentially-tricky customer requests but in the pre-sale cycle though a great way to propose future-value, cost-benefit of any customized/calculated values should be seriously considered before the promise is made.

###End 7/26/18
