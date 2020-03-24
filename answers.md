### Prerequisites - Setup the environment ###

I Chose to go the basic environment path to prevent any issues as was recommended.  I am all ready a VirtualBox and Vagrant user on my host machine (basic .DMG installer as I am a Mac user)
  
Started a new Project Folder with the Vagrant Image I like to keep my Host clean
	$ mkdir datadog
	$ cd datadog
	$ vagrant init hashicorp/bionic64
	$ vagrant up
  
  ![Alt Text](https://github.com/joeyhowe/images/blob/master/01.png)
  ![Alt Text](https://github.com/joeyhowe/images/blob/master/02.png)
  
The next thing I went ahead and just added the LAMP stack to bare vm in that order Apache, MySql and PHP.  I know some of this will come up in other sections.

Apache install

$ sudo apt-get update
$ sudo apt-get install apache2
$ sudo service apache2 status

![Alt Text](https://github.com/joeyhowe/images/blob/master/03.png)


MySql Install

$ sudo apt-get install mysql-server

PHP Install

$ sudo apt-get install php libapache2-mod-php php-mysql
$ sudo nano /etc/apache2/mods-enabled/dir.conf

Added index.php to be the default in order of precedence in dir.conf

Restart Apache

$ sudo systemctl restart apache2

Default system setup is complete!
Signed up for DataDog though the trial as requested and added the agent to the host with the new installer

$ DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=5702725b2062c2b84ef82df95dabac4c bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)”

![Alt Text](https://github.com/joeyhowe/images/blob/master/04a.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/04.png)

### Collecting Metrics ###

Adding a “platform” tag

$ sudo nano /etc/datadog-agent/datadog.yaml

![Alt Text](https://github.com/joeyhowe/images/blob/master/05.png)

I Installed the DB (MySql) earlier, I used the agent instructions to add the required user and modified the config file in the the mysql.d file

![Alt Text](https://github.com/joeyhowe/images/blob/master/06.png)


Custom agent check I installed a template config for my_metric in /etc/datadog-agent/config.d/my_metric.d

Built the corresponding yaml file in the checks.d folder

![Alt Text](https://github.com/joeyhowe/images/blob/master/08.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/07.png)

Changed the collection interval
Bonus Question: I changed the collection interval by adding  -min_collection_interval: 45 to the custom check yaml file.
![Alt Text](https://github.com/joeyhowe/images/blob/master/10.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/11.png)



### Visualizing Data: ###

Timeboard.py script

> from datadog import initialize, api  
>   
> options = {"api_key": "5702725b2062c2b84ef82df95dabac4c", "app_key":"f5b2f31ce1105c45a5f20d0304c5da638680  
> ab4b" }  
> initialize(**options)  
> title = "Timeboard"  
> description = "my_metric"  
> graphs = [{  
>     "definition": {  
>         "events": [],  
>         "requests": [  
>             {"q": "avg:my_metric.gauge{*}"}  
>         ],  
>         "viz": "timeseries"  
>     },  
>     "title": "my_metric OverTime"  
> }, {  
>     "definition": {  
>         "events": [],  
>         "requests": [  
>             {"q": "anomalies(avg:mysql.net.aborted_connects{host:vagrant}, 'basic', 3)"  
>              }],  
>         "viz": "timeseries"  
>     },  
>     "title": "Database connect anomalies"  
> }, {  
>     "definition": {  
>         "events": [],  
>         "requests": [  
>             {"q": "avg:my_metric.gauge{*}.rollup(sum, 3600)"}  
>         ],  
>         "viz": "query_value"  
>     },  
>     "title": "Hourly Rollup Sum of my_metric"  
> }]  
> template_variables = [{  
>     "name": "vagrant",  
>     "prefix": "host",  
>     "default": "host:vagrant"  
> }]  
>   
> read_only = True  
> api.Timeboard.create(title=title,  
>                      description=description,  
>                      graphs=graphs,  
>                      template_variables=template_variables,  
>                      read_only=read_only)  


![Alt Text](https://github.com/joeyhowe/images/blob/master/09.png)

Bonus Question:
Anomaly detection is an algorithmic feature that identifies when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. 


### Monitoring Data ###

I used the interface to configure the my_metric monitor as requested

I configured the custom message and notification

![Alt Text](https://github.com/joeyhowe/images/blob/master/12.png)

Notification email screenshot

![Alt Text](https://github.com/joeyhowe/images/blob/master/11b.png)

Bonus Question: I set up both outages 7pm-9am M-F & SAT-SUN below are screenshots of the configs and emails

![Alt Text](https://github.com/joeyhowe/images/blob/master/13.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/14.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/15.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/16.png)

### Collecting APM Data ###

$ sudo nano /etc/datadog-agent/datadog.yaml

/## @param use_dogstatsd - boolean - optional - default: true
/## Set this option to false to disable the Agent DogStatsD server.
/#
use_dogstatsd: true

/## @param dogstatsd_port - integer - optional - default: 8125
/## Override the Agent DogStatsD port.
/## Note: Make sure your client is sending to the same UDP port.
/#
dogstatsd_port: 8125

Restart the agent

Start the sample app with ddtrace (pip and ddtrace wasn’t in my path and I was being a little lazy)

$ ./ddtrace-run python ../../apm_flask.py

Traffic against the app

![Alt Text](https://github.com/joeyhowe/images/blob/master/17.png)


Screenshots from the ddtrace data collected in the Datadog portal

![Alt Text](https://github.com/joeyhowe/images/blob/master/18.png)
![Alt Text](https://github.com/joeyhowe/images/blob/master/19.png)

Bonus Question:
A Service is a collection of one or many components to deliver to an end user a response (web server, middleware, db).  A resource is an individual item that is required for that service or service components to operate.

### Final Question: ###
I’ll start by saying that I could come up with a lot of different uses for the Datadog agent, however one world situation popped right into my head.

I was working for a customer in the gaming/hospitality industry and they were basically having performance and downtime issues with a particular part of their business.  If you have ever been in a casino they have honors/rewards kiosk for customer loyalty.  Basically after an upgrade the kiosk were not behaving and they had 100 spread across the property (hotel, casino, shops, restaurants and mall).  They were trying to manage them with an agent-less monitoring solution from a central server just to tell if they were up or down.  At 136 MB and the ability to also provide app metric data while still being able to see which kiosk aren’t reporting……no brainer for me.








