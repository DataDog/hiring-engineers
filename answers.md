Level 1:

I set up my Datadog account with name Roger Berlind and e-mail rberlind@optonline.net. I actually set up my Datadog account with company "Job Seeker" before starting this interview exercise, but I was then able to change the name of the organization to "Datadog Recruiting Candidate" on the organization settings screen to better match the instructions and avoid any confusion.

Before starting the exercise, I deployed the Datadog agent on my Windows 7 laptop, Thorsby, and on an AWS EC2 instance with public DNS ec2-54-147-87-50.compute-1.amazonaws.com running Tomcat and MySQL on Ubuntu.  I also set up the AWS, EC2, Tomcat, and MySQL integrations on the Linux instance.

The Datadog agent is software that collects performance metrics and events from monitored hosts and technologies and sends them to Datadog's SaaS environment.  Users can then log into their Datadog account with a web browser and easily monitor and diagnose the performance of their cloud, hybrid, and on-premise infrastructure and the applications that run on it.  The agent is very lightweight and secure.

I added tags to the agent configuration file /etc/dd-agent/datadog.conf on my Linux host by uncommenting the tags line and setting tags to "env:dev, role:appserver, owner:roger".  I then restarted the agent with the command "sudo /etc/init.d/datadog-agent restart" to apply the tags to the agent and all integrations on that host.  Here is a screenshot of the tags on that host:
![Screenshot of custom tags for a host](/HostWithCustomTags.jpg?raw=true "Host with custom tags")
You can also use this [link](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=247596171) into my Datadog account.

As mentioned above, I had installed the MySQL integration on my Linux host to monitor the MySQL 5.6 database running on it before starting this exercise.  I also just configured the MySQL integration on my Windows laptop too. Here is a screenshot showing MySQL metrics in my account:
![Screenshot of MySQL Dashboard](/MySQLDashboard.jpg?raw=true "MySQL dashboard")
You can also use this [link](https://app.datadoghq.com/dash/integration/mysql?live=true&page=0&is_auto=false&from_ts=1479654185837&to_ts=1479668585837&tile_size=m&tpl_var_scope=host%3Ai-f1b5fb62) into my datadog account.


