###PREREQUISITES

I downloaded VirtualBox and Vagrant and spun up a VM (Virtual Machine).

![1](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/1.png)

I signed up for a DataDog 14-day free trial and followed instructions to run the DataDog Agent on my Vagrant VM.

![2](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/2.png)

###COLLECTING METRICS

I spent a bit of time familiarizing myself with the DD Agent, and eventually used ```sudo datadog-agent status``` command to find the config file path.

![3](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/3.png)

At first I wasn't able to edit the file so I installed vim.

![5](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/5.png)

Then I opened up the Agent config file (datadog.yaml) in a vim editor, added tags, and saved.

![6](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/6.png)

After restarting the Agent,

![7](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/7.png)

I checked the Host Map on the DataDog site to make sure the tags I added to the config file registered.

![8](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/8.png)

Then it was time for my PostgreSQL integration! To start, I installed Postgres on my VM,

![9](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/9.png)

then I followed directions to install DD on my PostgreSQL server.

![10](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/10.png)

With Postgres on my VM and DataDog on my Postgres server, the next step was to configure the DD agent to connect to the server. This involved editing the Postgres config folder within the DD Agent and renaming the file (it was originally postgres.yaml.example so I had to take out "example" to get it to work)

![11](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/11.png)

Then I used the ```sudo datadog-agent status``` command to confirm the integration check passed (I could tell it worked when I saw the Postgres header with info below).

![12](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/12.png)

#####Custom Check

Next step was writing my own custom check. I had to read a lot of documentation for this one, but eventually learned that I should be creating my own files. The first file I created was a config file which I housed in the ```conf.d``` directory in the agent.

![13](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/13.png)

The second was a check file which I created in ```checks.d```. The assignment was to create "a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000" so I used the boilerplate provided in the docs, and found a Python function that generates a random number. Pretty new to Python syntax so a bit of time spent on syntactical snafoos, but eventually it seemed to be working.

![14](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/14.png)

Then I went back into the config file and added a minimum interval (I believe this is the bonus, the way you change the collection interval without modifying the check file).

![15](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/15.png)

Afterwards I ran a test to see if the check was working, which it seemed to be.

![16](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/16.png)

###VISUALIZING DATA

I read through the API docs many times for guidance on making timeboards through an API call. The datadog 101 video on timeboards and screenboards was also quite helpful. I had never used curl, but liked the idea of making the call right in my terminal, so with the help of the API docs and curl docs, I eventually got the syntax to a place that resulted in a timeboard.

![17](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/17.png)

I used curl
1. to create a timeboard with my custom metric over the host

![18](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/18.png)

2. to create a timeboard with the rollup sum function applied

![20](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/20.png)

3. to create a timeboard with my Postgres metric and the anomaly function applied

![19](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/19.png)

Then I set the timeframe of each board to last 5 mins and sent myself a snapshot

![21](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/21.png)

Bonus: I think this anomaly detector is showing no abnormal metric trends in the last 5 minutes

![22](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/22.png)

###MONITORING DATA

After doing everything from the command line it was a relief to use the Datadog UI to set up a monitor with custom alerts.

![23](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/23.png)

Bonus: I scheduled some downtime for the alert

![24](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/24.png)

###COLLECTING APM DATA

The initial setup for getting APM to work was pretty straighforward. I enabled trace collection in ```datadog.yaml```, the Agent config file.

![25](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/25.png)

Then I needed to do a few things to set up for running the flask app w/ ddtrace:
1. I installed python and python-pip in a new folder in my Vagrant VM
2. I used pip to install flask
3. I pasted the flask app from the hiring challenge Readme into a new file

![26](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/26.png)

Then I used pip to install ddtrace and started running trace services  

![27](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/27.png)

This was a very frustrating time because I could see the app was sending info to ```http://0.0.0.0:5050``` but navigating to that URL in my browser was giving me a ```refused to connect``` error. After what felt like a million attempted workarounds, I found a comment from a nice person on StackOverflow.

![31](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/31.png)

So I uncommented the ```"forwarded_port"``` section of my Vagrantfile and added ```5050``` after ```host:``` and ```guest:``` and eventually the traces began to load.

![33](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/33.png)

![28](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/28.png)

![29](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/29.png)

![30](/Users/flatironschool/Development/code/data_dog/hiring-engineers/screenshots/30.png)

Bonus Question: Services and Resources are both metrics collected by APM. A service is a process or bunch of processes that do one distinct thing, i.e. a webapp admin service or a database service. A resource is an action for a service, i.e. a URL, or a database query.

###FINAL QUESTION: CREATIVE WAYS TO USE DATADOG?

It would be interesting to use DataDog to monitor the mood of a city. You could make a dashboard using APIs that track whatever metric you imagine means sadness/happiness like the number of mental health calls being made to 311, air quality index, or the number of ice creams sold.

Also interesting could be using Datadog alerts to monitor migration patterns. For example if you were alerted every time over 3,000 Americans between the ages of 20 and 30 relocate to a foreign country within one year. Or if 500 New Yorkers re-located to a different State within a month. You could make dashboards with those metrics side by side with things like the rate of unemployment, or cost of healthcare to really determine why people leave their homes.    
