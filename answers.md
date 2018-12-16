## Links

1. Link to [host-dashboard](https://app.datadoghq.com/dash/host/732018690?live=true&page=0&tile_size=m&is_auto=false&from_ts=1544806380000&to_ts=1544809980000)

2. Link to [MySQL-integration](https://app.datadoghq.com/dash/integration/12/mysql---overview?tile_size=m&page=0&is_auto=false&from_ts=1544806500000&to_ts=1544810100000&live=true)

3. Link to [Host-Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

4. Link to [My Monitors](https://app.datadoghq.com/monitors/manage)

5. Link to [Datadog-Docs](https://docs.datadoghq.com/)


*** All Screenshots are inline with the answers to the questions. ***

## Section 1: Prerequisites - Setup the environment
1. Spin up a Linux Virtual Machine using Vagrant and Virtual Box

   - Install VirtualBox
     - Link to [Install-VirtualBox](https://www.virtualbox.org/wiki/Downloads)
     - ![VirtualBox](./datadog-images/section-1/install-virtual-box.png)

   - Install Vagrant
     - Link to [Install-Vagrant](https://www.vagrantup.com/intro/getting-started/install.html)

     - After Installing Vagrant, you create a Vagrant file in the directory where you want to create your VM. You do this with the following command:  `$ vagrant init ubuntu/xenial64` .
    This clones the appropriate box, in my case an Ubuntu Linux 16.04 box.
     - Once the Vagrant file has been created properly, you can spin up your VM with the command: `vagrant up`
     - After the VM has spun up, you can enter the machine with the command: `vagrant ssh`
     - You now have access to the VM through the command line and can navigate around, install software and create and execute files.

2. Sign up for Datadog
   - Signing up for Datadog is super easy. Here is a screenshot of the form.
   - ![sign up](./datadog-images/section-1/signup-for-datadog.png)


3. Install the Agent on your VM and get it reporting metrics
   - To install the Datadog Agent on your VM
     - Datadog makes this really easy by giving you a link to the instructions in the **Getting Started Dropdown Menu**
     - There is a link there for **Install an Agent**
       - Link to [Install-Agent](https://app.datadoghq.com/account/settings#agent)
     - Here is a screenshot of the Installation Instructions:
       - ![install agent](./datadog-images/section-1/how-to-install-datadog-01.png)
     - Here you choose your OS, mine is Ubuntu.
     - After choosing your OS, you are given clear and easy instructions on how to install the Datadog Agent through your command line
     - Here is a screenshot of the instructions
       - ![install ubuntu](./datadog-images/section-1/ubuntu-install-instructions.png)


     - After running this in the command line of your VM, you should get two confirmations that the agent installed.
       - In the command line you should see something like this:
         - ![agent success cli](./datadog-images/section-1/data-dog-agent-success-command-line.png)


       - In the DataDog Web Portal you should see something like this:
         - ![agent success web portal](./datadog-images/section-1/data-dog-agent-web-portal-success-ws.png)


     - Finally, in the DataDog Web Portal you should see that you have a host sending data and your first metrics
       - ![host map](./datadog-images/section-1/host-reporting-data.png)


       - ![first metric](./datadog-images/section-1/first-datadog-metric.png)




## Section 2: Collecting Metrics
1. **Add tags in the Agent config file**
   - To add tags to the **Agent config file**, you can get instructions from the DataDog Documentation
   - You can get to the Docs by clicking on the **Question mark** on the homepage and selecting **Resources** from the Dropdown menu
   - On the **Resources** page select **Documentation** and this will take you to the **Documentation Page**

     - ![resources page](./datadog-images/section-2/resources-page-cropped.png)


   - On the Documentation Page, Click on **Tagging** and then **Assigning Tags**
     - ![assign tags](./datadog-images/section-2/assigning-tags-docs.png)


   - Here is a Link to those Docs: [DataDog-Tag-Docs](https://docs.datadoghq.com/tagging/assigning_tags/?tab=go)

   - In order to add tags, you have to edit the **datadog.yaml** file which is located on your VM in the **conf.d directory**. The path on Linux is: /etc/datadog-agent/datadog.yaml

   - In the **datadog.yaml** file, you add tags as key value pairs, an example would be `tags: <KEY_1>:<VALUE_1>, <KEY_2>:<VALUE_2>, <KEY_3>:<VALUE_3>`

   - Here is a screenshot of how to add the tags in the **datadog.yaml** file.
   - ![change yaml](./datadog-images/section-2/add-tags-yaml-file.png)


   - You can see the tags in the DataDog web portal in the **Host Map Page** which you can get to either through the **Infrastructure** menu by selecting **Host Map** or by clicking on **Expanded Host map**
   - Here is a screenshot of that:

   - ![get to host map](./datadog-images/section-2/how-to-get-to-host-map.png)

   - Here is a screenshot of my host and it's tags on the **Host Map** page
   - ![host and tags](./datadog-images/section-2/tags-ws.png)

2. **Install a database and Datadog Integration**
   - Installing a Database on a Vagrant VM can be done in many ways. I used this set of instructions for installing mySQL on Linux.
     - Link to [Install-Database](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04)

   - After the database is installed, you can install the Datadog Integration by following the instructions in the web portal

   - To get to those instructions you can either use the link in the **Get started** drop down or click on the **puzzle icon** and select **Integrations** from the drop down. Here is a screenshot of that:
   - ![integeration-01](./datadog-images/section-2/integration-01.png)

   - Select an Integration from the choices. I chose MySQL.

   - Datadog provides easy to follow instructions on how to set up the integration. Here are Screenshots of how to do that:
   - ![integeration-03](./datadog-images/section-2/integration-03.png)
   - ![integeration-04](./datadog-images/section-2/integration-04.png)
   - ![integeration-05](./datadog-images/section-2/integration-05.png)

   - After you have created a datadog user for your MySQL server, and granted the appropriate privileges, you configure the agent to connect to your database server in the **mysql.yaml** file located at **conf.d/mysql.yaml**.

   - Restart the agent and run the info command to make sure that the integration checks passed.

   - If everything is working properly, you should see this in the Datadog web portal
    - ![integeration-06](./datadog-images/section-2/integration-06.png)

3. **Create a custom Agent check which submits a metric named my_metric**
   - To create a custom Agent check, there is a set of instructions in the DataDog docs under **Developer Tools**
   - Here is a screenshot of that:
   - ![custom-agent-check-docs-01](./datadog-images/section-2/custom-agent-check-docs-01.png)
   - **Custom agent checks** are best for collecting metrics from custom apps.
   - In order to create a custom check we must create two files:
     - a **.yaml** file located `etc/datadog-agent/conf.d` directory
     - and a **.py** file located `etc/datadog-agent/checks.d` directory
     - These files names **MUST MATCH** (`my_check.yaml`, `my_check.py` for example) or the process will not work.
     - The **.yaml** file contains at a minimum a sequence called instances, that contains at least one mapping. An example would be: `instances: [{}]`
     - The **python file** for the check must inherit from the **AgentCheck Class**
     - Every custom check class needs a check method, inside of which we can use any of the built-in DogStatd methods. For this example, I am using the **gauge method**.

     - Here is a screenshot of the two files I created:
     - ![my_check.py](./datadog-images/section-2/mycheck-py.png)
     - ![my_check.yaml](./datadog-images/section-2/mycheck-yaml.png)

     - After you create these two files, you must **restart** the datadog agent for them to start sending metrics. You can then run the agent info request  and see if our check is running:

     - Here is a screenshot of that:
     - ![my_check.yaml](./datadog-images/section-2/custom-agent-check-working.png)

4. **Bonus: Can you change the collection interval without modifying the Python check file?**
   - Yes. You can modify the collection interval in the **.yaml** file as shown above.


## Section 3: Visualizing Data
1. **Utilize the Datadog API to create a Timeboard.**

   - In order to use the **DataDog API** to create a **Timeboard**, you must create a script that will send a POST request to the API
   - The instructions for how to do this can be found if you navigate to the **Datadog Help** page, and then click `API's for Developers`. This has documentation on how to use the API. If you click on **Timeboards**, you can get the code to create a script that will use the API to Create, Update and Delete Timeboards.

   - Here is a screenshot of that page:

   - ![create_timeboard](./datadog-images/section-3/create-timeboard-docs.png)

   - I created a **Python script,** that imported the Datadog API module for making API calls.
   - Here is a screenshot of that script.
   - ![create_timeboard](./datadog-images/section-3/create-timeboard-script.png)

   - In order to run the script, you need both an **API key and an Application key**.
   - You can find both of those keys under the **Integration Menu** if you select API's.
   - ![api-menu](./datadog-images/section-3/integrations-menu.png)

   - Here you can generate both API and Application Keys:
   - ![api-menu](./datadog-images/section-3/API-keys.png)

   - Once you have these keys, you can copy and paste them into your script and then run the script to create a **Timeboard** based on the variables in the script.
   - To specify specific metrics that you want on the **Timeboard**, you use the **requests** variable, with key value pairs representing the **request query** and the **type of metric** you want on the board.
   - For this challenge, I needed to create a **Timeboard** that has my custom metric scoped over my host, any metric from the Integration on my Database with the anomaly function applied, and my custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

   - Therefore, I used the following code in the script:
   - ![json](./datadog-images/section-3/json.png)

   - After running this script, the **Timeboard** is created and you have access to it through the Datadog web portal UI.
   - You can find it in your **Dashboard List.**
   - ![dashboard-menu](./datadog-images/section-3/dashboard-menu.png)
   - ![dashboard-list](./datadog-images/section-3/dashboard-list.png)
   - ![test-timeboard](./datadog-images/section-3/test-timeboard-1.png)

   - I Set the **Timeboard's** timeframe to the last 5 minutes and took a snapshot of this graph and used the @ notation to send it to myself.

   - Here is a screenshot of that:
   - ![snapshot](./datadog-images/section-3/timeboard-snapshot.png)

   - Here is a screenshot of the email I received:
   - ![email](./datadog-images/section-3/timeboard-email-2.png)

   - **Bonus Question: What is the Anomaly graph displaying?**
     - The **Anomaly graph** identifies strange behavior in a single metric based on the metric’s past performance. The algorithms it can use are: basic, agile, robust and adaptive.
     - Here is a link to more information about the Anomaly Graph:
     - - Link to [Anomaly Graph](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/)



## Section 4: Monitoring Data
1. **Create a Monitor**
   - In order to create a new monitor, you click on the **Create Monitor** button on the **Welcome Page**
   - ![create_monitor](./datadog-images/section-4/01-create-monitor.png)

   - Then you select the **Monitor type**, in this case, I chose **Metric**.
   - ![monitor-type](./datadog-images/section-4/02-select-monitor-type.png)

   - After that, you begin to configure the monitor by first selecting the **Detection Method**, in this case I chose **Threshold**
   - ![detection-method](./datadog-images/section-4/03-choose-detection-method.png)

   - Next, you choose the **Metric** you want to monitor, in my case, I chose my **custom metric**.
   - ![define-metric](./datadog-images/section-4/04-define-metric.png)

   - Now, you set your **Alert Conditions**, in my case I set the threshold levels and also to alert if there is no data for 10 minutes.
   - ![alert-conditions-2](./datadog-images/section-4/06-set-alert-conditions.png)

2. **Configure the Monitor's message**
   - After the alert conditions are set, you can configure the message that will be sent. You can use variables wrapped in double brackets to set what the message will be under different conditions.
   - `#` Indicates to run the message if the condition is **true**
   - `^` Indicates to run the message if the condition is **false**
   - An example is `{{#is_warning}}`
   - I set the message to display different information depending on if the Monitor was an `Alert`, `Warning`, or there was a `No Data` state.
   - I also used the variables to include the **metric value** that caused the Monitor to trigger and **host ip** when the Monitor triggers an Alert state.

   - Here is a screenshot of that configuration:
   - ![email-config-1](./datadog-images/section-4/07-email-configuration.png)

   - Finally, I configured who will be notified:
   - ![notify-team](./datadog-images/section-4/09-notify-team.png)

   - And here is a screenshot of the email notification I received:
   - ![email-notification](./datadog-images/section-4/10-email-screenshot.png)

3. **Bonus Question: Set up two scheduled downtimes for this monitor:**
   - One that silences it from 7pm to 9am daily on M-F
   - In order to schedule downtime for your monitors, you need to click on the **Manage Downtime** tab
   - ![manage-downtime-tab](./datadog-images/section-4/11-manage-downtime.png)

   - And then click on `Schedule Downtime`
   - ![schedule-downtime](./datadog-images/section-4/12-manage-downtime.png)

   - Then you determine what to silence and set up a schedule for that. You can choose a one time schedule or  a recurring schedule.
   - ![schedule-downtime](./datadog-images/section-4/13-choose-what-to-silence.png)
   - ![schedule-downtime](./datadog-images/section-4/14-downtime-schedule.png)
   - ![schedule-downtime](./datadog-images/section-4/15-downtime-schedule.png)

   - Then you configure the **downtime notification**:
   - ![downtime-message](./datadog-images/section-4/16-downtime-message.png)

   - This is a screenshot of the email notification:
   - ![18-downtime-email](./datadog-images/section-4/18-downtime-email.png)

   - I used the same instructions to create a second downtime that silences the monitor all day on Sat-Sun.
   - Here are the steps in screenshots:
   - ![19-second-downtime](./datadog-images/section-4/19-second-downtime.png)
   - ![20-second-downtime-schedule](./datadog-images/section-4/20-second-downtime-schedule.png)
   - ![21-second-downtime-message](./datadog-images/section-4/21-second-downtime-message.png)
   - ![23-second-downtime-email-confirmation](./datadog-images/section-4/23-second-downtime-email-confirmation.png)



## Section 5: Collecting APM Data

1. **Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:**
   - I used this Flask app and ran it from my VM
   - I instrumented the application by using `ddtrace-run`
   - After running the app, I navigated to each url.
   - Here is a screenshot of a Dashboard with both **APM and Infrastructure Metrics**
   - ![apm-dashboard](./datadog-images/section-5/apm-dashboard.png)

2. **Bonus Question: What is the difference between a Service and a Resource?**
   - A **Service** is a set of processes that do the same job. For instance, a simple web application may consist of two Services: A single webapp service and a single database service.
   - A **Resource** is a particular action for a Service. For a web application: some examples might be a URL, such as /user/about or a route in a MVC framework like Ruby. For a SQL database: a Resource is the query itself, such as SELECT * FROM users WHERE id = ?.




## Section 6: Creative Use for Datadog Question

I would use Datadog to monitor an app for Santa’s Naughty and Nice list. Parent’s could sign up for the app/platform and keep a daily record of whether their kids have been naughty or nice.  You could use Datadog to monitor the traffic and use integrations like AWS to spin up new instances of the app as heavier traffic came in. You could monitor the app’s traffic and use the time series data to see when most parents were submitting data.  You could use Datadog to Monitor, troubleshoot, and optimize application performance. By monitoring the performance of the cpu’s and the databases, you could make changes to the code to limit expensive database queries and find faster ways to interact with the database and the user. An in the end, you could create a Dashboard and share it around .. even with Santa. ;)
