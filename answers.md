//TODO: add a table of contents with links to question sections.
## Prerequisites - Setup the environment
Originally for this challenge I decided to set up my environment with Vagrant. I'm on a Windows 10 home OS I've used Vagrant before and really enjoyed it and I figured why not.
However, after setting up and making a vagrant box to share I decided to switch to AWS' cloud Linux vm. I've always wanted to try EC2 and running my vm on their cloud would save me space, cpu and work installing postgres.
 
-- You can still read about how I set up my vagrant [here](vagrantSetup.md)

### Setting up AWS Linux
Log into aws 
Navigate to the EC2 Dashboard from the Services drop down menu and Launch an Instance.
From there follow the directions on the Quick Start screen.
![select AMI](./screenshots/aws_linux_setup1.png) 
I chose the first option for my AMI because it came with Python and Postgres preloaded.

Next option was to chose the Instance type. 
Since this is a light tutorial the free tier t2 Micro should be more than fine.
![select Size](./screenshots/aws_linux_setup2.png)
Finally before my vm is created I created and downloaded a new key pair so that I can ssh into my vm from my local machine.
![generate key pem](./screenshots/aws_linux_setup3.png)

From here I had two ways I could access my VM from windows. 
Either through puTTy or through ssh in the Windows Sub-Linux(WSL). I'll be using the latter.

In the bash shell use the `chmod` command to make sure your private key file isn't publicly viewable
`chmod 400 /path/my-key-pair.pem`

Use the ssh command to connect to the instance. You specify the private key (.pem) file and user_name@public_dns_name. For example, if you used an Amazon Linux AMI, the user name is ec2-user. 
`sudo ssh -i /path/my-key-pair.pem ec2-user@ec2-198-51-100-1.compute-1.amazonaws.com`
you can find the public DNS address on your dashboard 
![dashboard](./screenshots/ec2_dashboard.png)

__warning: without `sudo` I got an 'unprotected private key file' error__
![private key file error](./screenshots/private_key_file_error.png)

SUDO!
![success](./screenshots/in_vm.png)
Success!!

 //TODO:  
## Collecting Metrics:

I installed the Datadog agent on Ubuntu with the easy one step install `DD_API_KEY=1852b8c40afd989d5e512340f1a0d3c8 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`
//TODO: insert picture of agent output
Agent v6 installed successfully and is running.
 
### Adding Tags to the Agent file:
    I navigated over to the agent config file located at `/etc/datadog-agent/datadog.yaml` (note: agent v6 will be a `.yaml` file and v5 is `.conf`)
    
    I checked out the `datadog.yaml.example` and the `datadog.yaml` too see how to format my tags. It looks like these files start off identical by default but it'll be good to have an unchanged example copy if I needed to ever revert back. 
    I uncommented the tags on `datadog.yaml` file and added a few of my own and saved.
    
        # Set the host's tags (optional)
         tags:
           - mytag
           - crystalball
           - env:dev
           - role:database:postgres
           
    I went onto my dashboard to see if my tags were there and didn't see any. I checked the dogs and didn't see another step requiring a restart. So then I tried to check the agent's config with ` sudo datadog-agent configcheck`
    I got the following error:
    
    ![agent config check error](./screenshots/config_check_error.png)
    
    
    
I went beck to investigate my yaml file. I see my api key is in there and not commented out on top. Since I am able to see my host on the dashboard but just not my new tags I started to doubt this is the kind of key it was referring too.
I went over to line 34 and it is my tags settings. After a quick search I found that some people have solved a similar error in other programs with indentation. I fixed the indentation in the file.

That solved the  agent config check error! However, the actual output wasn't helpful after all.
So, I decided to try restarting the agent thinking maybe the service should restart whenever you change the config file.

 It wasn't until I went to filter on the hostmap dashboard that I noticed My tags showed up.
    
   ![Screenshot of Tags in Host Map](screenshots/tags_hostmap.png)
    
Yay!
- [X]  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

### Integrating the database:
- [ ]  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

- [ ]  Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

- [ ]  Change your check's collection interval so that it only submits the metric once every 45 seconds.

- [ ]  **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
