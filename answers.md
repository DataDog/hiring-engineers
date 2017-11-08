## Prerequisites:

#### Creating a Vagrant VM
1. I installed Vagrant for Mac from https://www.vagrantup.com/downloads.html.
2. Per the Vagrant instructions, I also installed VirtualBox from https://www.virtualbox.org/.
3. Then, using Terminal, I started up their example virtual machine, which was their standard 64-bit Ubuntu VM.

![ss1](/images/ss1.png)

4. I was able to SSH into it successfully.

![ss2](/images/ss2.png)


#### Installing Datadog agent
1. I signed up for Datadog.
2. Next, I installed Docker for my VM while I was connected via SSH by following the instructions here: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#set-up-the-repository.
   a.	I ran into an issue where “add-apt-repository” command was not found and I had to run **sudo apt-get install software-properties-common python-software-properties**
3. I followed the instructions at https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce-1 to install the CE version of Docker.
   a.	I ran into an issue where I received the error: “Unable to locate package docker-ce” and it looks like Ubuntu 12.04 “precise” version is no longer supported (https://github.com/moby/moby/issues/31940).
   b.	Thus, I destroyed the VM and created a new one – Ubuntu/trusty64 - and restarted the instructions and was able to run hello-world successfully.
   c.	Then I used Datadog’s agent installation for Docker (https://app.datadoghq.com/signup/agent#docker), but ran into issue with permission denied.  However, using **sudo** resolved this.
4. I tried adding tags in the agent configuration file only to find out that the file wasn’t in etc/dd-agent-datadog.conf and instead I found it in three different locations:

![ss3](/images/ss3.png)

5. I decided to try again, not using Docker and using just the Ubuntu OS instead.  Thus I destroyed this VM using **vagrant destroy**, and started a new one.
6. I changed the hostname of the VM using the command **sudo hostname your-new-name** and rebooted using the command **shutdown -r now**.  After the reboot, I confirmed that the VM was seeing the new hostname.
7. Then I ran the one-step install for the agent for Ubuntu and it looked like it installed successfully.
8.	I was then able to see this new host in the host map and infrastructure list, but the old one was there as well.  However, from my research, it should disappear within a few hours.

![ss4](/images/ss4.png)


## Collecting Metrics:

#### Adding tags
1. I edited the file at etc/dd-agent/datadog.conf using **sudo nano datadog.conf** and added some tags.

![ss5](/images/ss5.png)

2. Then I stopped and started the datadog agent using **sudo /etc/init.d/datadog-agent stop** and **sudo /etc/init.d/datadog-agent start**.

![ss6](/images/ss6.png)

3.	I was able to see my tags updated on the host map:

![ss7](/images/ss7.png)


#### Installing database & Datadog integration
1. I installed MySQL on Ubuntu by running **sudo apt-get install mysql-server**.
2. Then I went to the **Integrations** link on the left sidebar in the Datadog web app and started following the installation instructions for the MySQL Integration.

![ss8](/images/ss8.png)

3. I ran into an issue where it would not let me create a new user for Datadog:

![ss9](/images/ss9.png)

4. I got into the mysql interface using **mysql -u root -p** and then input my root password, and followed through on the installation instructions within MySQL successfully.
5.  At the end, I was able to verify that the integration check had passed by using **sudo /etc/init.d/datadog-agent info**:

![ss10](/images/ss10.png)


#### Creating a custom agent
1. To write an agent check, I followed the documentation at https://docs.datadoghq.com/guides/agent_checks/, created their example "hello" check, and stopped and started the agent.
2. I then checked this was successful by running the info command, **sudo /etc/init.d/datadog-agent info**:

![ss11](/images/ss11.png)

3. I could also see the "hello" metric on the host map:

![ss12](/images/ss12.png)

4. Then I created my own metric called "my_metric" by first creating and editing a file called mymetric.yaml in the dd-agent/conf.d folder.

![ss13](/images/ss13.png)

5. I created and edited a file called mymetric.py in the dd-agent/checks.d folder.

![ss14](/images/ss14.png)

6. I stopped and restarted the agent and I was able to see the custom check in the info.

![ss15](/images/ss15.png)

7. I was also able to see this new metric in the host map:

![ss16](/images/ss16.png)

8. **Bonus Question:** I actually modified the yaml file, not thePython file to change the collection interval, so yes, I can change the interval without changing the Python file.


## Visualizing Data

#### Creating a Timeboard
1. To create a new timeboard, using the API, I first started by following the example in the documentation at https://docs.datadoghq.com/api/?lang=python#timeboards.
2. I also had to generate an application key at https://app.datadoghq.com/account/settings#api to use in the example Timeboard Python file.
3. I created a Python file and copied and pasted the example Python code into it and tried running it via **python timeboard.py**, but of course I got an error "ImportError: No module named datadog".
4. Since I am not too familiar with Python, I did some research on how to install the module and first installed pip, a package manager for Python, using the command, **sudo apt-get install python-pip**.
5. Then I installed the datadog package using **sudo pip install datadog** and then again tried running **python timeboard.py** and I was able to see the example Timeboard on my Datadog web app.

![ss17](/images/ss17.png)

6. I then modified the python file to create the dashboard that I needed:

      `from datadog import initialize, api

      options = {
          'api_key': 'c3c402f9691974bbac1ca439edf8b16a',
          'app_key': '111ecf89e7e7d2a5a5a59f57e7806897c195e79d'
      }

      initialize(**options)

      title = "Salome's Timeboard"
      description = "A timeboard created by the Salome"
      graphs = [{
        "definition": {
          "events": [],
          "requests": [
            {"q"   : "avg:my_metric.salome{host:ubuntu-try1-salomekbg}",
             "type": "line"},
            {"q"   : "avg:my_metric.salome{host:ubuntu-try1-salomekbg}.rollup(sum,60)",
             "type": "line"}
          ],
          "viz": "timeseries"
        },
        "title": "My_metric Information"
      },{
        "definition": {
          "events": [],
          "requests": [
            {"q"   : "anomalies(avg:mysql.net.connections{host:ubuntu-try1-salomekbg}, 'basic', 2)",
             "type": "line"}
          ],
          "viz": "timeseries"
        },
        "title": "MySQL net connections"
      }]

      template_variables = [{
        "name": "host1",
        "prefix": "host",
        "default": "host:ubuntu-try1-salomekbg"
        }]

      read_only = True

      api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)``

7. I checked the Dashboard on the Datadog web application and I was able to see the new dashboard with the two graphs in the dashboard:

![ss18](/images/ss18.png)

![ss19](/images/ss19.png)


#### Accessing the Dashboard
1. I then set the Timeboard's timeframe to the past five minutes by using the mouse and dragging on the graph from the right to the left until I selected five minutes worth of data.
2. I took a snapshot of each graph by clicking on the camera icon on the top right of each graph.

![ss20](/images/ss20.png)

3. When I clicked on the "Events" link on the left sidebar, I was able to see my snapshots and my annotations:

![ss21](/images/ss21.png)

4. **Bonus Question:** The Anomaly graph is supposed to display whenever a metric starts behaving differently than it has in the past, thus you can see change in a trend in your specified metric.  It would be best used with a metric that has established patterns, so that one can see the changes in behavior more easily.  (See https://docs.datadoghq.com/guides/anomalies/.)


## Monitoring Data

#### Creating a Monitor

1. I hovered over the "Monitors" link and clicked on the "New Monitor" link and filled out the information to create a new monitor for my_metric.

![ss22](/images/ss22.png)

![ss23](/images/ss23.png)

#### Configuring the Monitor

1. I edited the monitor to send me an email whenever the monitor gets triggered.

![ss24](/images/ss24.png)

2. I also added messages depending on what the status of the monitor is:

{{#is_alert}}My_metric is above 800!{{/is_alert}}

{{#is_alert_to_warning}}My_metric is down from 800 to 500, but is still too high.{{/is_alert_to_warning}}

{{#is_alert_recovery}}No need to be so alarmed, My_metric is now under 800.{{/is_alert_recovery}}

{{#is_warning}}This is a warning that My_metric just reached 500.{{/is_warning}}

{{#is_warning_recovery}}My_metric is now under 500.{{/is_warning_recovery}}

{{#is_no_data}}No data has been received for the last 10 minutes!{{/is_no_data}}

{{#is_no_data_recovery}}Data is now incoming from My_metric.{{/is_no_data_recovery}}

3. I updated all the messages to also send the value and the host IP address.

{{#is_alert}} My_metric is above 800!  It is currently at {{value}} and the host IP is {{host.ip}}. {{/is_alert}}

{{#is_alert_to_warning}} My_metric is down from 800 to 500, but is still too high.  It is currently at {{value}} and the host IP is {{host.ip}}. {{/is_alert_to_warning}}

{{#is_alert_recovery}} No need to be so alarmed, My_metric is now under 800.  It is currently at {{value}} and the host IP is {{host.ip}}. {{/is_alert_recovery}}

{{#is_warning}} This is a warning that My_metric just reached 500. It is currently at {{value}} and the host IP is {{host.ip}}. {{/is_warning}}

{{#is_warning_recovery}} My_metric is now under 500. It is currently at {{value}} and the host IP is {{host.ip}}. {{/is_warning_recovery}}

{{#is_no_data}} No data has been received for the last 10 minutes! {{/is_no_data}}

{{#is_no_data_recovery}} Data is now incoming from My_metric. {{/is_no_data_recovery}}

4. This is a screenshot of the alert email that I received:

![ss25](/images/ss25.png)

5. **Bonus Question** I scheduled downtime for the alert by going to the "Monitors" link on the sidebar and clicking the "Manage Downtime" link and I set up three recurring downtimes:

![ss26](/images/ss26.png)

![ss27](/images/ss27.png)

![ss28](/images/ss28.png)

![ss29](/images/ss29.png)

Email Notification screenshot:

![ss31](/images/ss31.png)


## Collecting APM Data

1. I followed the instructions here: https://app.datadoghq.com/apm/install, but got the error, "ImportError: cannot import name Flask".  I then installed Flask using the command, **sudo apt-get install python-flask** and then I was able to run the Python file, but the output I got stopped at "ddtrace.api - DEBUG - reported 1 services."  I am also seeing nothing in the APM section of my web app.  I also tried adding "apm_enabled: true" to datadog.conf file and restarting the agent, even though I believe that later versions of the agent do not need this added.  

2.  I also tried out the example code here: https://github.com/DataDog/dd-trace-py/blob/master/ddtrace/contrib/flask/__init__.py and still getting the same issues on terminal as well as nothing is showing up in the dashboard.

![ss30](/images/ss30.png)


3. **Bonus Question** The difference between a Service and a Resource is that while a Service is a group of processes that work together as an application, a Resource can be a query to a specific Service. (Refer to https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)


## Final Question

Since Datadog can help with monitoring traffic, it would be great if one of my favorite stores, The Uncommons, could have their foot traffic be monitored.  It's a fairly popular business and it can be fairly daunting to find a free table.  If the store had some sort of electronic register to monitor cash transactions, as well as monitor their credit card transactions, we could get a sense of their real-time foot traffic. Thus customers could work their timeframes to when they are more likely to find a table.  It would also help the store owners figure out why their influx of customers slow down and how to pick up business at those times.

I know that Google does measure "Popular Times" for a business, but from my understanding, it is using Google Maps to determine a person's location.  Using Datadog's monitoring can be more accurate by monitoring actual transactions, not just people who might happen to be near the store.
