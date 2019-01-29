Your answers to the questions go here.


Collecting Metrics:

Step 1) Access the Agent config file.

To add tags to your agent, you'll need to accees the configuration file.  The path to your configuration file depends on what platform you're using.  For a linux platform, the path is:
/etc/datadog-agent/datadog.yaml. 

If you get a 'denied access' error, try to 'cd' into each parent directory one at a time until you are in the datadog-agent file.  You can then 'ls' to see the files in that directory.  datadog.yaml should be in there.

From there, use vi to access the file from the command line and edit the file.  You can use the arrow keys to move down the file to the 'Set the host's tags' section and add your custom tag there. In my repo, I added a custom tag of 'env:development' for practice.

![add_tags](https://user-images.githubusercontent.com/38845846/51808195-8fabce80-2245-11e9-8d31-d6f26b07f1f3.png)

This is a screenshot of the host and it's new tag in the Host Map page.

Step 2) To install PostgreSQL on your virtual machine, you'll use the command 'apt-get install postgresql'.  Once you run that in the command line, you'll can return to datadog and access the postgresql integration from the integrations page (via the toolbar on the left).  

Click on Postgresql and install.  The configurations tab will give you an option to 'generate a password'.  Once you click that, start psql on your virtual machine and run the code provided in teh configuration instructions.  The second section of code is run after you exit psql.  Next, you'll edit conf.d/postgres.yaml file (in the /etc/datadog-agent/conf.d directory) to include the configuration provided with the password genrated for you.  Finally, you'll restart the agent and check the agent satus to ensure the integration has been correctly installed.

Step 3) Create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000 with a collection interval that it only submits the metric once every 45 seconds.

To do this, you'll again use vi to create a custom_check.py file under datadog-agent/check.d directory.  You'll also need to create a custom_check.yaml file in the datadog-agent/conf.d directory.  This is where you can modify the interval for the check you created in custom_check.py.

![screen shot 2019-01-28 at 4 45 09 pm](https://user-images.githubusercontent.com/38845846/51876035-2480fb80-231c-11e9-85ac-f555bf4fcf77.png)

Above is a screenshot of custom_check.py


Visualizing Data:

Timeboard snapshot:

To create a custom metric using Datadog's API, it's helpful to refer to the following documentation (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard).  Sample code that I used is below.  Note, you'll need to input your own API and APP keys, which can be found in your account info.

__________________________________________________________________
from datadog import initialize, api

options = {
    'api_key': '<<source your personal API key>>',
    'app_key': '<<source your personal APP key>>'
}

initialize(**options)

title = "Solutions Engineer Timeboard"
description = "Create a timeboard for hiring challenge"
graphs = [{
    "definition": {
        "events":[],
        "requests": [
            #these requests scope over the host we created, apply the 
            #anomolies function and the rollup function.  
            #Note, I had some difficulty with the synatax for these - 
            #reviewing them with a co-worker would be helpful for me!
            {"q": "avg:my_metric.data{host:trialhostname}"},
            {"q": "avg(last_1h):anomalies(avg:system.cpu.system{name:cassandra}, 'basic', 3, directions='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1"},
            {"q": "avt:random.data.rollup(sum,60)"}],
        "viz": "query_value"
    },
    "title": "Random Timeboard Trial"
}]

template_variables = [{
    "name": "host1", 
    "prefix": "host", 
    "default": "host:my-host"

}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


________________________________________________________________________

![screen shot 2019-01-28 at 11 33 07 am](https://user-images.githubusercontent.com/38845846/51861256-9e9b8b00-22f0-11e9-91ae-c1c4dd945699.png)



Monitoring Data:

To create a new monitor from the GUI, use the toolbar on the left and select new monitor from the montiors option.  Then click on 'Metric' to create your new monitor alert for my_metric.  Select 'my_metric.data' from the drop-down field, then enter your threshold conditions under 'Set alert conditions.'

New Alert Monitor screenshots:
![screen shot 2019-01-28 at 11 28 06 am](https://user-images.githubusercontent.com/38845846/51861025-056c7480-22f0-11e9-8228-fdf22e57455b.png)

![screen shot 2019-01-28 at 11 26 00 am](https://user-images.githubusercontent.com/38845846/51861054-1b7a3500-22f0-11e9-987d-327dc9c37108.png)

To configure the monitor's message to send an email and customized messages based on alert, use the documentation found here:  https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning.  The conditional variables will allow you to control what message is sent, depending on the alert/warning/no-data conditions.  Using @ notification will allow you to control who recieves the messages. 


To schedule downtime when you do not want to recieve alerts, click on the 'Manage Downtime' tab on the middle of you GUI.  The 'Schedule Downtime' button on the right will allow you to set when you do not want to recieve notifications (and indicate which users are affected by this downtime).

Downtime for scheduled alert:
![screen shot 2019-01-28 at 11 27 45 am](https://user-images.githubusercontent.com/38845846/51861015-feddfd00-22ef-11e9-809b-53d78e7150f0.png)

![screen shot 2019-01-28 at 11 25 43 am](https://user-images.githubusercontent.com/38845846/51861037-0ef5dc80-22f0-11e9-9ad3-77efb7b0a65c.png)


Collecting APM Data:

First, go to your conf.yaml file and ensure that the amp_config is set to 'enabled:true'.  Next, configure your environment.  Your 'env:' tag under apm_confg in your conf.yaml file can be reset here, or will inherit from the 'env:development' tag that was set in step 1.  

FIX THIS PART.

Bonus:
A service is the name of a set of processes that work together to provide a feature set, for example a webapp service or a database service.  A resource is a specific query to a service.  More information can be found at: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-

Creative ways to use Datadog:
I have chickens.  It would be interesting to use Datadog to monitor the conditions in which they produce eggs.  For example, how does temperature affect when they lay?  Does food type impact the size or frequency of eggs?  What about light (i.e. season/day length).  It would be cool to see all this broken down using Datadog.

