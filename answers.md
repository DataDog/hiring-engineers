# Datadog - Solutions Engineer Technical Exercise

![](https://datadog-prod.imgix.net/img/dd_logo_70x75.png?fm=png&auto=format&lossless=1)

Datadog is a comprehensive monitoring, reporting, and visualization suite for seamlessly integrating the monitoring needs of your infrastructure and application in one place.  Datadog allows you to easily build complex reporting metrics, visualizations, and alerts using the Datadog Agent and your web browser.

# Part I - Collecting Data

### Create your Datadog account

The first step to gaining invaluable insight into your application and infrastructure is to sign up for a Datadog account [here](https://datadoghq.com).  It's a quick and easy process with no credit card required.

![](https://d3dr1ze7164817.cloudfront.net/items/1X3n1X1X0Q070q2d3L0e/Image%202017-06-12%20at%2010.35.39%20AM.png?v=c5a973bb)

Click 'Get Started Free', enter your information, and submit the form.

![](https://d3dr1ze7164817.cloudfront.net/items/122M0r2j3w0o2W0k1x3b/Image%202017-06-12%20at%2010.37.00%20AM.png?v=6db9fe41)

Datadog will ask you a few questions about your stack and the needs of your organization. This is to help you get up and running as quickly as possible.

![](https://d3dr1ze7164817.cloudfront.net/items/101K001v3q2M023f1a1V/Screen%20Recording%202017-06-12%20at%2010.42%20AM.gif?v=086236b1)

### Installing and configuring the Agent

The next step is to install the Datadog Agent.  The Agent is a lightweight application that helps Datadog collect important metrics from your environment to provide easy and comprehensive monitoring.  It listens to the pulse of your infrastructure and application, sending the metrics to Datadog for analysis.

![](https://d3dr1ze7164817.cloudfront.net/items/0J2y3A2H1I111S0r1o0f/Image%202017-06-12%20at%2010.43.20%20AM.png?v=8f7a515b)

Select your environment from the list of options and use Datadog's easy script for a pain-free install.

![](https://d3dr1ze7164817.cloudfront.net/items/453I142w1q0N370E0J3S/Image%202017-06-12%20at%2010.45.36%20AM.png?v=8639d5ee)

Once installed, the Agent will immediately begin collecting metrics from your environment.

![](https://d3dr1ze7164817.cloudfront.net/items/0o1R2m2x0D0E2P09300I/Image%202017-06-12%20at%2010.46.03%20AM.png?v=bc0b5524)

You can customize each host by adding tags to the Agent config file.  This allows us to create unique tags for different environments, streamlining the process of reporting.  Open the config file (/etc/dd-agent/datadog.conf) in your favorite editor.

```sh
sudo vim /etc/dd-agent/datadog.conf
```

Add tags that identify the environment or application you are monitoring with this instance of the agent.  Use the format 'tags: key:value, key:value' to make the tags more descriptive.

![](https://d3dr1ze7164817.cloudfront.net/items/3A10433J0E3i082c1w1M/Image%202017-06-12%20at%2011.08.38%20AM.png?v=11e7d302)

Once you have saved your configuration file, restart the Agent using the following command:

```sh
sudo /etc/init.d/datadog-agent restart
```

Now that the Agent is up and running with some custom tags, return to Datadog in your browser and expand your host map.

![](https://d3dr1ze7164817.cloudfront.net/items/2p2I2B0W1O2L3O160B3F/Image%202017-06-12%20at%201.47.54%20PM.png?v=3157e8f6)

Click on your host to drill-down into expanded view.  You should now see the details of your host along with the tags you created in the config file.

![](https://d3dr1ze7164817.cloudfront.net/items/25233T2N1V1U0c2s3o2K/%5Be2a6e7d51c3dc5bc2b93281d135800ee%5D_Image%25202017-06-12%2520at%252011.15.17%2520AM.png?v=5b4f1a63)

### Installing a database integration

Datadog offers dozens of integrations out of the box to provide customized metrics for your environment.  Let's continue by installing the PostgreSQL integration.

The first step is to create a read-only postgres user for Datadog.  Connect to your postgres instance with superuser privileges and execute the following:

```sh
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
```

To confirm that the permissions have been created correctly, you can execute this command from the shell.

```sh
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

It should return a single row query result.

![](https://d3dr1ze7164817.cloudfront.net/items/3a3d0m3U1b3F2v3u0A0r/Image%202017-06-12%20at%2011.26.22%20AM.png?v=fd29b1bc)

Now let's configure the agent to monitor your postgres instance.  We configure the agent by editing YAML files located in /etc/dd-agent/conf.d/.  Navigate to the directory, copy the postgres.yaml.example file to postgres.yaml, and open it in your favorite editor.

```sh
cd /etc/dd-agent/conf.d/
sudo cp postgres.yaml.example postgres.yaml
sudo vim postgres.yaml
```

In the config file, enter the connection information for your database instance and set 'collect_function_metrics' to True.

![](https://d3dr1ze7164817.cloudfront.net/items/0A0W0v3S0e0l3r092c1j/%5B304704d7665cd8e302134efc70145859%5D_Image%25202017-06-12%2520at%252011.42.50%2520AM.png?v=06270f2a)

Save the file and restart the agent.

```sh
sudo /etc/init.d/datadog-agent restart
```

Within a few minutes your host detail view in Datadog should show the collection of PostgreSQL metrics from your instance.  It was that easy!

![](https://d3dr1ze7164817.cloudfront.net/items/1K162C3z353I3u0t3G3J/%5B3766ec8f92957c01fb5b3a81dfa14f83%5D_Image%25202017-06-12%2520at%252011.43.30%2520AM.png?v=d5c30870)

### Creating a custom Agent check

Much of Datadog's value comes from how easy it is to customize for your own application. Writing your own Agent check in Python only requires configuring a single YAML file in addition to your Python script.

For this example, we are going to create an Agent check that sends a random number to our Datadog account every 30 seconds.  First, we will write our script using Datadog's AgentCheck class, part of the checks library that is delivered with the Agent.

All custom checks need to live in /etc/dd-agent/checks.d/.  Let's navigate to that directory and open up a new file in our editor.

```sh
cd /etc/dd-agent/checks.d/
sudo vim random.py
```

We will create our custom check by creating a new class, RandomCheck, that inherits from AgentCheck.  We will then use Python's random to generate a random number and send it as a metric to Datadog.

```sh
import random
from checks import AgentCheck  # Import AgentCheck from the checks library

class RandomCheck(AgentCheck):  # Create our new class, inheriting from AgentCheck
    def check(self, instance):  # Define the check method
        name = 'test.support.random'  # Give our metric a unique name for reporting
        val = random.random()  # Generate a random number
        self.gauge(name, val)  # Send our metric to Datadog
```

Once we have saved our script, we are going to create a configuration file to let the Agent know to execute it.  The configuration file goes along the other config files in /etc/dd-agent/conf.d/

```sh
cd /etc/dd-agent/conf.d/
sudo vim random.yaml
```

We are going to create a minimal configuration for our new check and only specify 'min_collection_interval: 30' to tell the Agent to only run the script once every 30 seconds.

```sh
init_config:
    min_collection_interval: 30

instances:
    [{}]
```

Restart the Agent after saving the file.

```sh
sudo /etc/init.d/datadog-agent restart
```

Let's view the status of the Agent to make sure it is recognizing the new check.

```sh
sudo /etc/init.d/datadog-agent info
```

We should see our new check 'random' listed in the Agent info.

![](https://d3dr1ze7164817.cloudfront.net/items/2n0H291e1Z2j1c230Y2s/%5B3eb9d39d16f2434195c6be576d633ac1%5D_Image%25202017-06-12%2520at%252012.08.49%2520PM.png?v=eca938f1)

Returning to our host map, we see the new metric reporting under Apps > test.

![](https://d3dr1ze7164817.cloudfront.net/items/2F1Y1h2X3F1B3D0S0z32/%5Bd7b5d330d15eba13bf3cb6de172dfc00%5D_Image%25202017-06-12%2520at%25203.07.30%2520PM.png?v=4f9d8c33)

So far, we have installed the Datadog Agent on our server, configured the PostgreSQL database integration, created our custom agent check, and witnessed the metrics populating our host map.  In the next section, we are going to continue by visualizing the great data we are capturing.

# Part II - Visualizing your Data

Datadog provides best-in-industry data visualizations in an easy drag-and-drop interface. Datadog's dashboard tools provide two default formats for your visualizations, the Timeboard and the Screenboard.  When creating a new dashboard, use a TimeBoard if you intend to use it for troubleshooting issues and correlating metrics and events from different layers of your stack.  If you want to visualize system status and provide general reporting, use a ScreenBoard.

### Customizing our integration dashboard

When using integrations, Datadog comes with pre-built dashboards out-of-the-box to help you obtain quick insights into your infrastructure.  Let's use the auto-generated PostgreSQL dashboard to create a new, customized dashboard that incorporates all of the metrics we are collecting.

From your Datadog console select the dashboard icon and click 'Dashboard List' > select the 'Postgres - Overview' dashboard.

![](https://d3dr1ze7164817.cloudfront.net/items/34230c2p05130g2M0B2h/%5Bfba12755c41a38957ba446c3eb0d7b55%5D_Image%2525202017-06-12%252520at%25252012.17.03%252520PM.png?v=3c093cdd)

Select 'Clone Dashboard' from the settings menu.

![](https://d3dr1ze7164817.cloudfront.net/items/0S0c0p3P3C3l3x2z080Q/Image%202017-06-12%20at%2012.17.30%20PM.png?v=2d092042)

Enter a new name and a description for your dashboard and commence cloning.

![](https://d3dr1ze7164817.cloudfront.net/items/1q1t1N2p322f47222213/Image%202017-06-12%20at%2012.19.10%20PM.png?v=da3eed7a)

Let's customize a pre-existing graph by adding a metric to an existing Timeseries graph.  Click the edit icon on the 'Connections' graph > select 'Add Metric' > choose 'postgresql.commits' from the drop-down and click 'Save'.

![](https://d3dr1ze7164817.cloudfront.net/items/2W1B3G2G04012v08103H/Screen%20Recording%202017-06-12%20at%2012.37%20PM.gif?v=c9a5b816)

Creating new visualizations is just as easy.  Let's create a graph for our custom random number metric.

Scroll down and click the 'Add a graph' link at the bottom of the dashboard > drag the icon for Timeseries graph to the indicated area > choose 'test.support.random' for the metric > optionally add a title, and save the new graph.

![](https://d3dr1ze7164817.cloudfront.net/items/2D3n3G050H230S442D25/Screen%20Recording%202017-06-12%20at%2012.32%20PM.gif?v=3b826ca3)

### Collaborating through visualization

Collaboration and communication are built right into Datadog's application.  You can quickly create shareable annotations and send them to your team without leaving your dashboard.  Here we identify a spike on our graph and annotate it.  Our comment is immediately sent to our coworker using the @notifications syntax.  There is no need to switch to your email or another application, Datadog integrates with the most common collaboration utilities including Slack and HipChat.

![](https://d3dr1ze7164817.cloudfront.net/items/012v2m0T193J3z2d2a2b/Screen%20Recording%202017-06-12%20at%2003.47%20PM.gif?v=7ffe67bd)

# Part III - Alerting on your Data

No monitoring suite would be complete without the ability to send alerts.  Datadog's alerting capabilities are robust and easy to use.

Remember the spike that we identified on our random number metric?  Let's create an alert to notify us if this occurs again.

From the your console toolbar select Monitor > New Monitor > and select 'Metric' as the monitor type.

![](https://d3dr1ze7164817.cloudfront.net/items/0i0j2m2w2f2f210e3A3e/Image%202017-06-12%20at%2012.41.13%20PM.png?v=20e90240)

Define your metric by using 'test.support.random' in the 'Get' field.  Also, use the 'Multi Alert' option for each 'host' to allow this alert to be scaled across all hosts in your environment.

![](https://d3dr1ze7164817.cloudfront.net/items/1V3s3y1X0h1R1G0U1431/%5B17b017265e428f1c28f7ed45a64ef5c6%5D_Image%25202017-06-12%2520at%252012.43.53%2520PM.png?v=56f0e414)

Use Markdown to customize the message of your alert.  You may want to include a link to your dashboard in the message.

![](https://d3dr1ze7164817.cloudfront.net/items/1E0X0I0Y3Q143g0l0Z04/Image%202017-06-12%20at%2012.54.44%20PM.png?v=2a294efd)

Now that your alert is configured, whenever the threshold is exceeded you will be notified.  In this example, we have been notified by email.

![](https://d3dr1ze7164817.cloudfront.net/items/2l3u0x3U1M1l3p0y093Z/Image%202017-06-12%20at%201.39.24%20PM.png?v=7c992659)

By default, alerts will be sent 24 hours a day.  There are many circumstances when you would want to suppress an alert during off-hours.  To schedule downtime navigate to the Monitors tab and click 'Manage Downtime' > 'Schedule Downtime'.

![](https://d3dr1ze7164817.cloudfront.net/items/0i1O2e101n0w30230O3D/Image%202017-06-12%20at%2012.58.42%20PM.png?v=245889c4)

Configure your downtime by selecting your monitor from the drop-down.  Then choose a schedule, in this case we want to silence the monitor from 7PM to 9AM and repeat daily with no end date.

![](https://d3dr1ze7164817.cloudfront.net/items/1X471V2H1g2z3l2I3o3b/Image%202017-06-12%20at%2012.58.04%20PM.png?v=f832aea8)

Add a message to describe why the downtime is being scheduled > select which members of your team you would like to notify > and Save.

![](https://d3dr1ze7164817.cloudfront.net/items/2y3j0c1i3j0n120c0s0B/Image%202017-06-12%20at%204.27.26%20PM.png?v=3e5899dd)

This concludes our overview of Datadog.  In a few minutes we were able to connect our application to best-in-class monitoring using the Datadog agent, the built-in PostgreSQL integration, and our own custom Agent check. 

Dashboard: https://app.datadoghq.com/dash/302258

Note: Did not receive emails from 'Notify your team' when scheduling downtime or using @notification when creating the annotation.

