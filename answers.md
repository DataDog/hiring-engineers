Prerequisites - Setup the environment

I installed Vagrant and went with the latest Ubuntu LTS

C:\Users\James>vagrant box add ubuntu/bionic64
==> box: Loading metadata for box 'ubuntu/bionic64'
    box: URL: https://vagrantcloud.com/ubuntu/bionic64
==> box: Adding box 'ubuntu/bionic64' (v20181129.0.0) for provider: virtualbox
    box: Downloading: https://vagrantcloud.com/ubuntu/boxes/bionic64/versions/20181129.0.0/providers/virtualbox.box
    box: Download redirected to host: cloud-images.ubuntu.com
    box: Progress: 100% (Rate: 8424k/s, Estimated time remaining: --:--:--)
==> box: Successfully added box 'ubuntu/bionic64' (v20181129.0.0) for 'virtualbox'!

Added the following to the Vagrantfile
Vagrant.configure(2) do |config|
config.vm.box = "ubuntu/bionic64"
config.vm.provider "virtualbox" do |vb|
vb.memory = "2048"
end

![Vagrantfile](Vagrantfile)

C:\Users\James>vagrant up
C:\Users\James>vagrant ssh

Note: I obfuscated the API keys with ***** in this and other submitted files.

Installed the Datadog agent
DD_API_KEY=***** bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"


Collecting Metrics:
	Adding Tags:
vagrant@ubuntu-bionic:~$ sudo vim /etc/datadog-agent/datadog.yaml
Added the following-
tags:
  - env:exercise
  - instance:bionic
  - name:mongodb-host

![datadog.yaml](datadog.yaml)
![Screenshot](screenshots/tags.jpg)

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB for this part of the exercise

vagrant@ubuntu-bionic:~$ sudo apt install mongodb
vagrant@ubuntu-bionic:~$ mongo
> use admin
switched to db admin
> db.createUser({
...   "user":"datadog",
...   "pwd": "ddpass",
...   "roles" : [
...     {role: 'read', db: 'admin' },
...     {role: 'clusterMonitor', db: 'admin'},
...     {role: 'read', db: 'local' }
...   ]
... })
> exit

vagrant@ubuntu-bionic:~$ sudo vim /etc/datadog-agent/conf.d/mongo.d/conf.yaml
Added the following-
  init_config:
  instances:
  - server: mongodb://datadog:ddpass@localhost:27017/admin
    additional_metrics:
      - collection       # collect metrics for each collection
      - metrics.commands
      - tcmalloc
      - top

![conf.yaml](conf.yaml)
![Screenshot](screenshots/mongo.jpg)

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

vagrant@ubuntu-bionic:~$ sudo vim /etc/datadog-agent/checks.d/randcheck.py
vagrant@ubuntu-bionic:~$ sudo vim /etc/datadog-agent/conf.d/randcheck.yaml
vagrant@ubuntu-bionic:~$ sudo systemctl restart datadog-agent
vagrant@ubuntu-bionic:~$ sudo -u dd-agent -- datadog-agent status

![randcheck.py](randcheck.py)
![randcheck.yaml](randcheck.yaml)
![Screenshot](screenshots/random.jpg)

Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes, since the interval is specified in the associated yaml file  - min_collection_interval: 45


Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

vagrant@ubuntu-bionic:~$ sudo apt install python-pip
vagrant@ubuntu-bionic:~$ pip install datadog
vagrant@ubuntu-bionic:~$ vim python.py
vagrant@ubuntu-bionic:~$ python timeboard.py

![timeboard.py](timeboard.py)
![Screenshot](screenshots/timeboard.jpg)
https://app.datadoghq.com/dash/1007353/exercise-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1544062140000&to_ts=1544065740000&live=true

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

![Screenshot](screenshots/timeboard.jpg)

Bonus Question: What is the Anomaly graph displaying?
It highlights outlying datapoints outside of expected patterns.


Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![Screenshot](screenshots/metricmonitor.jpg)
![Screenshot](screenshots/metricmonitoremail.jpg)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Screenshot](screenshots/weeklydowntime.jpg)
![Screenshot](screenshots/weekenddowntime.jpg)

Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

vagrant@ubuntu-bionic:~$ sudo pip install flask
vagrant@ubuntu-bionic:~$ sudo vim /etc/datadog-agent/datadog.yaml
Added the following-
apm_config:
  enabled: true
  
vagrant@ubuntu-bionic:~$ sudo systemctl restart datadog-agent
vagrant@ubuntu-bionic:~$ ddtrace-run python flask_app.py

![Screenshot](screenshots/trace1.jpg)
![Screenshot](screenshots/trace2.jpg)

Bonus Question: What is the difference between a Service and a Resource?
A service is the name of a set of processes that work together to provide a feature set whereas a resource is a particular query to a service.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![Screenshot](screenshots/APM_Infrastructure_Dashboard.jpg.jpg)
https://app.datadoghq.com/dash/1007452/apm-and-infrastructure-metrics?tile_size=m&page=0&is_auto=false&from_ts=1544062140000&to_ts=1544065740000&live=true

Please include your fully instrumented app in your submission, as well.
![flask-app.py](flask-app.py)


Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I'd use it for weather monitoring and forecasting.  I've created a dashboard that monitors the temperature in NYC as a quick exercise.
https://app.datadoghq.com/dash/1011718/weather?tile_size=m&page=0&is_auto=false&from_ts=1544065920000&to_ts=1544069520000&live=true
![Screenshot](screenshots/weather.jpg)
![weather.py](weather.py)


