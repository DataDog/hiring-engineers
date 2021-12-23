If you want to apply as a Solutions or Sales Engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.


<a href="https://www.datadoghq.com/careers/" title="Careers at Datadog">
<img src="https://imgix.datadoghq.com/img/careers/careers_photos_overview.jpg" width="1000" height="332"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Once this is ready, sign up for a trial Datadog at https://www.datadoghq.com/

**Please make sure to use “Datadog Recruiting Candidate” in [the “Company” field](https://a.cl.ly/wbuPdEBy)**

Then, get the Agent reporting metrics from your local machine and move on to the next section...

For the environment setup I had a Windows 10 JUMPBOX machine and a Windows Server 2016 in an Azure subscription.
I also created an Ubuntu 18.04 VM in Azure which I then installed the Datadog agent on.

![image](images/1.PNG?raw=true "1")

![image](images/2.PNG?raw=true "2")

For Windows 2016 I simply installed the Datadog agent MSI and followed the instructions.
Since I saw Datadog had a specific Azure section when installing the Agent I decided that for my personal subscription I would like to see the process of linking my Azure subscription to Datadog.
For this I followed the steps here : https://docs.datadoghq.com/integrations/azure/?tab=azurecliv20#setup
I first logged in to my Azure tenant

![image](images/3.PNG?raw=true "3")

I then proceeded with creating an App Registration in my Azure AD named Datadog Auth.

![image](images/4.PNG?raw=true "4")


And also, a client secret for the registration

![image](images/95.png?raw=true "95")

I followed the documentation further by creating a user with Monitoring Reader role in the Subscriptions IAM

![image](images/5.png?raw=true "5")


I then went to the Azure integration and added the information needed from my subscription and added the registration.

![image](images/6.PNG?raw=true "6")


The add came back successful

![image](images/7.PNG?raw=true "7")


After the integration I went to add the Datadog Agent as an extension to my VMs in Azure.

![image](images/8.png?raw=true "8")

I then validated this was functional by going to the Azure VM Default Dashboard.

![image](images/9.png?raw=true "9")


The machines also appeared in my host app. I added a second subscription that I have from work just to see how the host map looked and also installed the MSI agent on two of those machines.

![image](images/10.png?raw=true "10")



## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

A quick google of the Agent config file location /etc/datadog-agent/datadog.yaml
I then quickly added some tags both on the Windows VM and the Ubuntu VM by looking at the following example on Github from the eDocs 
https://github.com/DataDog/datadog-agent/blob/main/pkg/config/config_template.yaml
For Windows I simply added environment, name and geo as shown below in the datadog.yaml file

![image](images/11.PNG?raw=true "11")


I am not sure if the next step is necessary but I restarted the Agent service just to ensure it made the changes.

![image](images/12.PNG?raw=true "12")


On Ubuntu a similar process was done but with VIM.I was having some issues for a little bit with the formatting. It seemed for some reason it did not like the formatting of the tags, I assume this was due to the spacing, however I copy pasted the exact format from the Windows machine notepad and just changed the values to make a distinction.

![image](images/13.PNG?raw=true "13")


I then restarted the agent service (again I am not sure if this step is necessary but it seemed to have worked for me)

![image](images/14.PNG?raw=true "14")


I then checked both machines and the tags were added successfully

![image](images/15.PNG?raw=true "15")

![image](images/16.png?raw=true "16")


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

For this step I installed MySQL on the Ubuntu VM 

![image](images/17.PNG?raw=true "17")

![image](images/18.PNG?raw=true "18")
 
 
 The next step was checking if I needed a separate agent for this integration. A quick check on the eDocs showed the following:
 
 ![image](images/19.PNG?raw=true "19")


I then just simply proceeded by adding the integration per the instructions on the MySQL Integration eDocs by running the following commands.

![image](images/20.PNG?raw=true "20")

![image](images/21.PNG?raw=true "21")

![image](images/22.PNG?raw=true "22")

![image](images/23.PNG?raw=true "23")


I then went to the mysql.d/conf.yaml file and edited it by comparing it to the sample mysql.d/conf.yaml file already present.

![image](images/24.PNG?raw=true "24")

![image](images/25.PNG?raw=true "25")


The integration was added successfully.
I then restarted the Agent service and ran a bunch of simple queries on the db. I then went to the MySQL Overview and saw traffic in the dashboard.

![image](images/26.PNG?raw=true "26")


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

For this section I looked at the following link: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

In here it talks about creating a Custom agent check. From this I took the hello.py sample code from the eDocs.

I then pasted this sample code into visual studio and looked up the random function syntax in python. I followed the syntax from here. 
https://www.programiz.com/python-programming/examples/random-number

I added a tag from my ubuntu machine and saved the file. I then copied the changes and pasted it in /etc/datadog-agent/checks.d/datatest.py

![image](images/27.PNG?raw=true "27")


I then followed the docs further and created a yaml file called datatest.yaml and pasted the sample code with the only change being the min_collection_interval from 30 to 45 in /etc/datadog-agent/conf.d

![image](images/28.PNG?raw=true "28")


I then ran the following test command on my datatest to check that the code executes properly

![image](images/29.PNG?raw=true "29")

I also went to the Datadog app and created a dashboard with my_metric data in order to see if this integration worked.

![image](images/30.PNG?raw=true "30")

![image](images/31.PNG?raw=true "31")

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

This was done in the previous step. Originally the sample file had a value of 30 and that was just simply changed to 45.

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Looking at the “Writing checks that run command line programs” eDocs. 
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
It suggests you can create a custom check that runs a command line program and captures its output as a custom metric. You could then use the command line to set the “min_collection_interval” value.
We can also do it as in the exercise by editing the conf.d file rather than the python.


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

The main doc I used for this is here: 
https://docs.datadoghq.com/api/latest/dashboards/
First, I Installed the Datadog API Collection. I was trying to get the key Authentication to validate the API and got a status code of 200 where all I added was the API Key to the Authorization.


![image](images/32.PNG?raw=true "32")

![image](images/33.PNG?raw=true "33")

![image](images/34.PNG?raw=true "34")

The status code was 200 when running the create dashboard however when I checked the Datadog App for the new dashboard it was not being created.

![image](images/35.png?raw=true "35")

![image](images/36.png?raw=true "36")

I’m not sure why the dashboard wasn’t being created. I spent some time troubleshooting this and, in the end, I just decided to start my own request from scratch rather than using the API Collection.
I repeated the same process and this time I got a different output for Validating the API key but still status code 200.

And when I ran the create dashboard POST call it also returned status 200.I used the code from the below eDocs in the body to test the creation of a test dashboard.
https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard

This also worked properly this time with a status code of 200 and more readable output than what I was previously getting. 

![image](images/37.png?raw=true "37")

![image](images/38.png?raw=true "38")

When I then checked the Dashboard list I could see the newly created Dashboard from the API.

![image](images/39.png?raw=true "39")

* Your custom metric scoped over your host.

![image](images/40.png?raw=true "40")

* Any metric from the Integration on your Database with the anomaly function applied.

https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/

![image](images/41.png?raw=true "41")

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

https://docs.datadoghq.com/dashboards/functions/rollup/

![image](images/42.png?raw=true "42")

I entered the body in the request and it came back successfully.

![image](images/43.png?raw=true "43")

I then checked the Dashboard List and saw it was created

![image](images/44.png?raw=true "44")

![image](images/45.png?raw=true "45")

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

![image](images/46.png?raw=true "46")

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![image](images/47.png?raw=true "47")

![image](images/48.png?raw=true "48")

* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

I entered the values in the question in the Monitor details shown below

![image](images/49.png?raw=true "49")


Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![image](images/50.png?raw=true "50")

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![image](images/51.png?raw=true "51")

I wanted to check if the value parameter was actually working as in the test, it shows as 0.0
I created the monitor and waited and I soon got a warning that shows the following.

![image](images/52.png?raw=true "52")

The value is now filled in which suggests it works.


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  
 ![image](images/53.png?raw=true "53")
  
  * And one that silences it all day on Sat-Sun.
  
  ![image](images/54.png?raw=true "54")
  
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
![image](images/55.PNG?raw=true "55")
  
  <img>
  

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```
I have had some previous experience in college with Flask so I spent a bit of time looking through the documentation in the references section..

I firstly installed Flask,

$ sudo pip3 install Flask

I then ran the app using the code that I was given above and it ran without an issue.

<img>

I was able to reach the endpoint on port 5050

<img>


* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

I ran into some issues getting ddtrace setup. I was missing some dependencies. A quick google search told me I needed to have python-setuptools installed. I installed it using the following command:
sudo apt-get install python-setuptools

I had to also import a Cython module as I was getting the following error
<img>

I installed the cython module

<img>

After this I as able to install ddtrace without any issue and the app started to run using the command given
DD_SERVICE="flaskservice" DD_ENV="ubuntudev" DD_LOGS_INJECTION=true ddtrace-run python flaskapp.py

<img>

I then accessed it again on the endpoint and I could logs appear on the service

<img>

I then restarted the datadog agent and waited a few minutes as the eDocs suggest. When I went back to the datadog app I was able to see the flask service there and was able to go into it.

<img>

<img>



* **Bonus Question**: What is the difference between a Service and a Resource?

A service is a piece of software that performs certain tasks. For example system services that are running on start-up in order to keep the key software services running for the endpoint to operate functionally.
A resource is more related to hardware but with cloud it can also be virtual not just physical. These are the bare bones of the computer system such as Disk, RAM, CPU info etc. These resources allow services to operate.


Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Link to Dashboard: https://p.datadoghq.eu/sb/0f546c48-5c07-11ec-87a1-da7ad0900005-7babdbc6c304146e166ec45bdd02399c


Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Since the initial look at datadog I was interested to see if I could integrate this with Citrix technology. As I have good experience working with the Citrix ADC (Netscaler) I wanted to try and see if I could integrate the datadog agent into it.
I believe this would be a challenge since under the hood of the Netscaler is a very customized FreeBSD OS that would prevent a lot of integrations that are pre-added in the initial image.
I first tried my hand at installing the Agent using the Debian/Ubuntu command on the eDocs.
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=24001504bc5544c28b23d0a157d7939c DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
It however was not a surprise to find that even though it ran, the package wasn’t installed. I checked the file directory on the Netscaler and no datadog folder was created.

<img>

Since this is a VM running in Azure, I thought maybe I could install the agent as an extension.

<img>

Even though I did that, the process was stuck on deployment which leads me to believe this is again not going to work.

<img>

I then decided to potentially try just putting the files on the Netscaler myself with WinSCP. I believe I have more of a chance running this as source rather than Ubuntu/Linux however it’s worth a shot.

<img>

Unfortunately, that did not work either, I did find some extra articles to try out however it could be too optimised however it would be part of the next steps.
I found a FreeBSD package for datadog-agent on GitHub that could be very useful if combining it with the missing dependencies on the NetScaler.
https://github.com/DataDog/dd-agent/issues/350#

Something else that could be a possibility is looking into the NITRO API: https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/
Nevertheless, I would be very interested to spend some time looking into this further as I believe a lot of customers I currently work with that have large Citrix environments would benefit massively from the in-depth monitoring and integrations that Datadog has available.



## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
